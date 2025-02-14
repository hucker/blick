"""Trivial Typer App to run Blick checks on a given target."""

import json
import pathlib
import sys

import typer
import uvicorn
import blick_api
import blick


s = pathlib.Path('./src').resolve()
sys.path.insert(0, str(s))

# Declare at top of file so  decorators work as expeted.
app = typer.Typer(add_completion=False)


def dump_results(results):
    """Dump results to stdout"""
    for result in results:
        typer.echo(result)


def pretty_print_json(json_obj):
    """
    Pretty print a JSON object, converting non-string values to strings.

    Args:
        json_obj (dict): The JSON object to be pretty printed.

    Returns:
        str: The pretty printed JSON string.
    """

    def convert_non_strings(obj):
        if isinstance(obj, dict):
            return {k: convert_non_strings(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_non_strings(elem) for elem in obj]
        else:
            return str(obj)

    pretty_json = json.dumps(convert_non_strings(json_obj), indent=4)
    return pretty_json


@app.command()
def run_checks(
        module: str = typer.Option(None, '-m', '--mod', help='The module to run rules against.'),
        pkg: str = typer.Option(None, '--pkg', help='The package to run rules against.'),
        json_file: str = typer.Option(None, '-j', '--json', help='The JSON file to write results to.'),
        flat: bool = typer.Option(False, '-f', '--flat', help='Should the output be flat or a hierarchy.'),
        score: bool = typer.Option(False, '-s', '--score', help='Print the score of the rules.'),
        api: bool = typer.Option(False, '-a', '--api', help='Start FastAPI.'),
        port: int = typer.Option(8000, '-p', '--port', help='FastAPI Port'),
        verbose: bool = typer.Option(False, '-v', '--verbose', help='Enable verbose output.'),
):
    """Run Blick checks on a given package or module from command line."""

    try:
        mod = None
        if module:
            target_path = pathlib.Path(module)
            if target_path.is_file():
                mod = blick.BlickModule(module_name=target_path.stem, module_file=str(target_path))
            else:
                typer.echo(f'Invalid module: {module} is not a file.')

        if pkg:
            folder = pathlib.Path(pkg)
            if folder.is_dir():
                pkg = blick.BlickPackage(folder=folder)
            else:
                typer.echo(f'Invalid package: {pkg} is not a folder.')

        # If they supply 1 or both they are all run since the checker can handle arbitrary combinations
        if mod or pkg:
            ch = blick.BlickChecker(modules=mod, packages=pkg, auto_setup=True)
            if api:
                blick_api.set_blick_checker(ch)
                uvicorn.run(blick_api.app, host='localhost', port=port)
                return
            else:
                results = ch.run_all()
        else:
            typer.echo('Please provide a module, package to run checks on.')
            return

        if not results:
            typer.echo('There were no results.')
            return

        if not flat:
            # Show the results in a hierarchy rather than the flat version the data is stored as.
            results = blick.blick_result.group_by(results, ['pkg_name', 'module_name', 'func_name'])
            pretty_data = pretty_print_json(results)
            typer.echo(pretty_data)
            return

        if verbose:
            dump_results(results)
        else:
            typer.echo(blick.overview(results))

        if score:
            test_score = blick.ScoreByResult()
            typer.echo(f'Score: {test_score(results):.1f}')

        if json_file:
            d = blick.blick_result.results_as_dict(results)
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(d, f, indent=2)

    except blick.BlickException as e:
        typer.echo(f'BlickException: {e}')

    # Crude
    except Exception as e:
        typer.echo(f'An error occurred: {e}')


if __name__ == '__main__':
    app()
