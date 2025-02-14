"""
These the rc factory method allowing fairly easily to have various flavors or RC files to
be interchangeable.

"""

import pytest

from blick import BlickMarkup
from blick import blick_format

def test_format_exc():
    with pytest.raises(ValueError):
        _ = BlickMarkup(open_delim='<@>', close_delim='<@>')

@pytest.mark.parametrize("tag,func,input,expected_output", [
    (blick_format.TAG_BOLD, BlickMarkup().bold, "Hello, World!", "<<b>>Hello, World!<</b>>"),
    (blick_format.TAG_ITALIC, BlickMarkup().italic, "Hello, World!", "<<i>>Hello, World!<</i>>"),
    (blick_format.TAG_UNDERLINE, BlickMarkup().underline, "Hello, World!", "<<u>>Hello, World!<</u>>"),
    (blick_format.TAG_STRIKETHROUGH, BlickMarkup().strikethrough, "Hello, World!", "<<s>>Hello, World!<</s>>"),
    (blick_format.TAG_CODE, BlickMarkup().code, "Hello, World!", "<<code>>Hello, World!<</code>>"),
    (blick_format.TAG_PASS, BlickMarkup().pass_, "Hello, World!", "<<pass>>Hello, World!<</pass>>"),
    (blick_format.TAG_FAIL, BlickMarkup().fail, "Hello, World!", "<<fail>>Hello, World!<</fail>>"),
    (blick_format.TAG_SKIP, BlickMarkup().skip, "Hello, World!", "<<skip>>Hello, World!<</skip>>"),
    (blick_format.TAG_WARN, BlickMarkup().warn, "Hello, World!", "<<warn>>Hello, World!<</warn>>"),
    (blick_format.TAG_EXPECTED, BlickMarkup().expected, "Hello, World!", "<<expected>>Hello, World!<</expected>>"),
    (blick_format.TAG_ACTUAL, BlickMarkup().actual, "Hello, World!", "<<actual>>Hello, World!<</actual>>"),
    (blick_format.TAG_RED, BlickMarkup().red, "Hello, World!", "<<red>>Hello, World!<</red>>"),
    (blick_format.TAG_BLUE, BlickMarkup().blue, "Hello, World!", "<<blue>>Hello, World!<</blue>>"),
    (blick_format.TAG_GREEN, BlickMarkup().green, "Hello, World!", "<<green>>Hello, World!<</green>>"),
    (blick_format.TAG_PURPLE, BlickMarkup().purple, "Hello, World!", "<<purple>>Hello, World!<</purple>>"),
    (blick_format.TAG_ORANGE, BlickMarkup().orange, "Hello, World!", "<<orange>>Hello, World!<</orange>>"),
    (blick_format.TAG_YELLOW, BlickMarkup().yellow, "Hello, World!", "<<yellow>>Hello, World!<</yellow>>"),
    (blick_format.TAG_BLACK, BlickMarkup().black, "Hello, World!", "<<black>>Hello, World!<</black>>"),
    (blick_format.TAG_WHITE, BlickMarkup().white, "Hello, World!", "<<white>>Hello, World!<</white>>"),
])
def test_all_tags(tag, func, input, expected_output):
    assert func(input) == expected_output


@pytest.mark.parametrize("markup_func,input,expected_output", [
    (BlickMarkup().bold, "Hello, World!", "Hello, World!"),
    (BlickMarkup().italic, "Hello, World!", "Hello, World!"),
    (BlickMarkup().underline, "Hello, World!", "Hello, World!"),
    (BlickMarkup().strikethrough, "Hello, World!", "Hello, World!"),
    (BlickMarkup().code, "Hello, World!", "Hello, World!"),
    (BlickMarkup().data, "Hello, World!", "Hello, World!"),
    (BlickMarkup().expected, "Hello, World!", "Hello, World!"),
    (BlickMarkup().actual, "Hello, World!", "Hello, World!"),
    (BlickMarkup().fail, "Hello, World!", "Hello, World!"),
    (BlickMarkup().warn, "Hello, World!", "Hello, World!"),
    (BlickMarkup().skip, "Hello, World!", "Hello, World!"),
    (BlickMarkup().pass_, "Hello, World!", "Hello, World!"),
    (BlickMarkup().red, "Hello, World!", "Hello, World!"),
    (BlickMarkup().blue, "Hello, World!", "Hello, World!"),
    (BlickMarkup().green, "Hello, World!", "Hello, World!"),
    (BlickMarkup().purple, "Hello, World!", "Hello, World!"),
    (BlickMarkup().orange, "Hello, World!", "Hello, World!"),
    (BlickMarkup().yellow, "Hello, World!", "Hello, World!"),
    (BlickMarkup().black, "Hello, World!", "Hello, World!"),
    (BlickMarkup().white, "Hello, World!", "Hello, World!")
])
def test_blick_render_text(markup_func, input, expected_output):
    render_text = blick_format.BlickRenderText()
    formatted_input = markup_func(input)
    assert render_text.render(formatted_input) == expected_output


@pytest.mark.parametrize("markup_func,input,expected_output", [
    (BlickMarkup().bold, "Hello, World!", "**Hello, World!**"),
    (BlickMarkup().italic, "Hello, World!", "*Hello, World!*"),

    (BlickMarkup().strikethrough, "Hello, World!", "~~Hello, World!~~"),
    (BlickMarkup().code, "Hello, World!", "`Hello, World!`"),
    (BlickMarkup().pass_, "Hello, World!", "`Hello, World!`"),
    (BlickMarkup().fail, "Hello, World!", "`Hello, World!`"),
    (BlickMarkup().warn, "Hello, World!", "`Hello, World!`"),
    (BlickMarkup().skip, "Hello, World!", "`Hello, World!`"),
    (BlickMarkup().expected, "Hello, World!", "`Hello, World!`"),
    (BlickMarkup().actual, "Hello, World!", "`Hello, World!`"),
    # For color markups in markdown, we assume BlickBasicMarkdown 
    # does no formatting, hence the expected output is plain text.
    (BlickMarkup().red, "Hello, World!", "Hello, World!"),
    (BlickMarkup().blue, "Hello, World!", "Hello, World!"),
    (BlickMarkup().green, "Hello, World!", "Hello, World!"),
    (BlickMarkup().purple, "Hello, World!", "Hello, World!"),
    (BlickMarkup().orange, "Hello, World!", "Hello, World!"),
    (BlickMarkup().yellow, "Hello, World!", "Hello, World!"),
    (BlickMarkup().black, "Hello, World!", "Hello, World!"),
    (BlickMarkup().white, "Hello, World!", "Hello, World!"),
    (BlickMarkup().underline, "Hello, World!", "Hello, World!"),
])
def test_blick_basic_markdown(markup_func, input, expected_output):
    markdown_render = blick_format.BlickBasicMarkdown()
    formatted_input = markup_func(input)
    output = markdown_render.render(formatted_input)
    assert output == expected_output


@pytest.mark.parametrize("markup_func,input,expected_output", [
    (BlickMarkup().bold, "Hello, World!", "[bold]Hello, World![/bold]"),
    (BlickMarkup().italic, "Hello, World!", "[italic]Hello, World![/italic]"),
    (BlickMarkup().underline, "Hello, World!", "[u]Hello, World![/u]"),
    (BlickMarkup().strikethrough, "Hello, World!", "[strike]Hello, World![/strike]"),
    (BlickMarkup().code, "Hello, World!", "Hello, World!"),
    (BlickMarkup().pass_, "Hello, World!", "[green]Hello, World![/green]"),
    (BlickMarkup().fail, "Hello, World!", "[red]Hello, World![/red]"),
    (BlickMarkup().warn, "Hello, World!", "[orange]Hello, World![/orange]"),
    (BlickMarkup().skip, "Hello, World!", "[purple]Hello, World![/purple]"),
    (BlickMarkup().expected, "Hello, World!", "[green]Hello, World![/green]"),
    (BlickMarkup().actual, "Hello, World!", "[green]Hello, World![/green]"),
    (BlickMarkup().red, "Hello, World!", "[red]Hello, World![/red]"),
    (BlickMarkup().blue, "Hello, World!", "[blue]Hello, World![/blue]"),
    (BlickMarkup().green, "Hello, World!", "[green]Hello, World![/green]"),
    (BlickMarkup().purple, "Hello, World!", "[purple]Hello, World![/purple]"),
    (BlickMarkup().orange, "Hello, World!", "[orange]Hello, World![/orange]"),
    (BlickMarkup().yellow, "Hello, World!", "[yellow]Hello, World![/yellow]"),
    (BlickMarkup().black, "Hello, World!", "[black]Hello, World![/black]"),
    (BlickMarkup().white, "Hello, World!", "[white]Hello, World![/white]"),
])
def test_blick_basic_rich(markup_func, input, expected_output):
    rich_render = blick_format.BlickBasicRichRenderer()
    formatted_input = markup_func(input)
    output = rich_render.render(formatted_input)
    assert output == expected_output


@pytest.mark.parametrize("markup_func,input,expected_output", [
    (BlickMarkup().bold, "Hello, World!", "<b>Hello, World!</b>"),
    (BlickMarkup().italic, "Hello, World!", "<i>Hello, World!</i>"),
    (BlickMarkup().underline, "Hello, World!", "<u>Hello, World!</u>"),
    (BlickMarkup().strikethrough, "Hello, World!", "<s>Hello, World!</s>"),
    (BlickMarkup().code, "Hello, World!", "<code>Hello, World!</code>"),
    (BlickMarkup().pass_, "Hello, World!", '<span style="color:green">Hello, World!</span>'),
    (BlickMarkup().fail, "Hello, World!", '<span style="color:red">Hello, World!</span>'),
    (BlickMarkup().skip, "Hello, World!", '<span style="color:purple">Hello, World!</span>'),
    (BlickMarkup().warn, "Hello, World!", '<span style="color:orange">Hello, World!</span>'),
    (BlickMarkup().expected, "Hello, World!", '<span style="color:green">Hello, World!</span>'),
    (BlickMarkup().actual, "Hello, World!", '<span style="color:red">Hello, World!</span>'),
    (BlickMarkup().red, "Hello, World!", '<span style="color:red">Hello, World!</span>'),
    (BlickMarkup().blue, "Hello, World!", '<span style="color:blue">Hello, World!</span>'),
    (BlickMarkup().green, "Hello, World!", '<span style="color:green">Hello, World!</span>'),
    (BlickMarkup().purple, "Hello, World!", '<span style="color:purple">Hello, World!</span>'),
    (BlickMarkup().orange, "Hello, World!", '<span style="color:orange">Hello, World!</span>'),
    (BlickMarkup().yellow, "Hello, World!", '<span style="color:yellow">Hello, World!</span>'),
    (BlickMarkup().black, "Hello, World!", '<span style="color:black">Hello, World!</span>'),
    (BlickMarkup().white, "Hello, World!", '<span style="color:white">Hello, World!</span>'),
])
def test_blick_basic_html_renderer(markup_func, input, expected_output):
    html_renderer = blick_format.BlickBasicHTMLRenderer()
    formatted_input = markup_func(input)
    output = html_renderer.render(formatted_input)
    assert output == expected_output


@pytest.mark.parametrize("markup_func, input, expected_output", [
    (BlickMarkup().bold, "Hello, World!", "**Hello, World!**"),
    (BlickMarkup().italic, "Hello, World!", "*Hello, World!*"),
    (BlickMarkup().strikethrough, "Hello, World!", "Hello, World!"),
    (BlickMarkup().code, "Hello, World!", "`Hello, World!`"),
    (BlickMarkup().pass_, "Hello, World!", ":green[Hello, World!]"),
    (BlickMarkup().fail, "Hello, World!", ":red[Hello, World!]"),
    (BlickMarkup().skip, "Hello, World!", ":purple[Hello, World!]"),
    (BlickMarkup().warn, "Hello, World!", ":orange[Hello, World!]"),
    (BlickMarkup().expected, "Hello, World!", ":green[Hello, World!]"),
    (BlickMarkup().actual, "Hello, World!", ":green[Hello, World!]"),
    (BlickMarkup().red, "Hello, World!", ":red[Hello, World!]"),
    (BlickMarkup().green, "Hello, World!", ":green[Hello, World!]"),
    (BlickMarkup().blue, "Hello, World!", ":blue[Hello, World!]"),
    (BlickMarkup().yellow, "Hello, World!", ":yellow[Hello, World!]"),
    (BlickMarkup().orange, "Hello, World!", ":orange[Hello, World!]"),
    (BlickMarkup().purple, "Hello, World!", ":purple[Hello, World!]"),
    (BlickMarkup().black, "Hello, World!", ":black[Hello, World!]"),
    (BlickMarkup().white, "Hello, World!", ":white[Hello, World!]"),

])
def test_blick_basic_streamlit_renderer(markup_func, input, expected_output):
    streamlit_renderer = blick_format.BlickBasicStreamlitRenderer()
    formatted_input = markup_func(input)
    output = streamlit_renderer.render(formatted_input)
    assert output == expected_output


@pytest.mark.parametrize("markup_func", [
    BlickMarkup().bold,
    BlickMarkup().italic,
    BlickMarkup().underline,
    BlickMarkup().strikethrough,
    BlickMarkup().code,
    BlickMarkup().pass_,
    BlickMarkup().fail,
    BlickMarkup().expected,
    BlickMarkup().actual,
    BlickMarkup().red,
    BlickMarkup().green,
    BlickMarkup().blue,
    BlickMarkup().yellow,
    BlickMarkup().orange,
    BlickMarkup().purple,
    BlickMarkup().black,
    BlickMarkup().white,
])
def test_blick_render_text_with_empty_string(markup_func):
    """All markups with null inputs should map to null outputs."""
    render_text = blick_format.BlickRenderText()
    input = ""
    expected_output = ""
    formatted_input = markup_func(input)
    output = render_text.render(formatted_input)
    assert output == expected_output
