import pathlib
import textwrap

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def format_response(response):
    new_response = response.replace("*", "")
    new_response = new_response.replace(":", ":\n")
    new_response = new_response.replace("：", "：\n")
    return new_response