import re
import sys
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

regex = re.compile(r"^(\s*)<!--Inject markdown here  -->", re.MULTILINE)


def execute():
    text = None
    markdown = None
    with open('template.html', 'r') as file:
        text = file.read()

    with open('example.md', 'r') as file:
        markdown = file.read()

    m = regex.search(text)
    markdown = re.sub(r"^", m.group(1), markdown, flags=re.MULTILINE)

    span = m.span(0)
    text = text[:span[0]] + markdown + text[span[1]:]

    with open('index.html', 'w') as file:
        file.write(text)


class MyHandler(PatternMatchingEventHandler):
    def dispatch(self, event):
        if (event.event_type == "modified" and event.src_path == ".\\example.md"):
            print(".\\example.md changed")
            execute()


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = MyHandler(patterns=["./example.md"])
    observer = Observer()

    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    execute()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
