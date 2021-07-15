import json
import tkinter
from typing import Any, Callable


class Labels(tkinter.Frame):
    def __init__(self, master: tkinter.Tk) -> None:
        super().__init__(master)

        self.pack()
        self.create_widget()

    def create_widget(self) -> None:
        url_entry = tkinter.Label(self, text="Repository URL")
        url_entry.grid(row=0, column=0)

        separator = tkinter.Label(self, text=":")
        separator.grid(row=0, column=1)

        name_entry = tkinter.Label(self, text="ProjectName")
        name_entry.grid(row=0, column=2)


class RepoEntry(tkinter.Frame):
    def __init__(self, master: tkinter.Tk, delete: Callable[[], Callable[[Any], None]]) -> None:
        super().__init__(master)

        self.url = tkinter.StringVar()
        self.name = tkinter.StringVar()
        self.delete = delete
        self.pack()
        self.create_widget()

    def create_widget(self) -> None:
        url_entry = tkinter.Entry(self, textvariable=self.url)
        url_entry.grid(row=0, column=0, ipadx=150)

        separator = tkinter.Label(self, text=":")
        separator.grid(row=0, column=1)

        name_entry = tkinter.Entry(self, textvariable=self.name)
        name_entry.grid(row=0, column=2, ipadx=50)

        delete = tkinter.Button(self, text="X")
        delete.grid(row=0, column=3)
        delete.bind("<ButtonPress>", self.delete())


class EmailEntry(tkinter.Frame):
    def __init__(self, master: tkinter.Tk) -> None:
        super().__init__(master)

        self.email = tkinter.StringVar()
        self.pack()
        self.create_widget()

    def create_widget(self) -> None:
        email_label = tkinter.Label(self, text="Enter email")
        email_label.grid(row=0, column=0)
        separator = tkinter.Label(self, text=":")
        separator.grid(row=0, column=1)

        email_entry = tkinter.Entry(self, textvariable=self.email)
        email_entry.grid(row=0, column=2, ipadx=50)


class Buttons(tkinter.Frame):
    def __init__(
        self,
        master: tkinter.Tk,
        load: Callable[[], None],
        add: Callable[[], None],
        save: Callable[[], None]
    ) -> None:
        super().__init__(master)
        self.target = tkinter.StringVar()
        self.load = load
        self.add = add
        self.save = save
        self.pack()
        self.create_widget()

    def create_widget(self) -> None:
        target_entry = tkinter.Entry(self, textvariable=self.target)
        target_entry.grid(row=0, column=0, ipadx=150)
        save_button = tkinter.Button(self, text="load", command=self.load)
        save_button.grid(row=0, column=1)
        add_button = tkinter.Button(self, text="add", command=self.add)
        add_button.grid(row=0, column=2)
        save_button = tkinter.Button(self, text="save", command=self.save)
        save_button.grid(row=0, column=3)


class Main():
    def __init__(self) -> None:
        self.num = 1
        self.repos: list[RepoEntry] = []
        self.settings: dict[str, Any] = {}
        self.email_entry: EmailEntry

    def add_row(self) -> None:
        self.repos.append(RepoEntry(self.root, self.delete_row))

    def save_json(self) -> None:
        """ output json file
        """
        target = self.button.target.get()
        _repos = []
        # Parse every lines
        for repo in self.repos:
            _url = repo.url.get().strip().replace("\\", "/")
            if _url == "":
                # Skip row there is no url
                continue

            _name = repo.name.get()
            if _name == "":
                # Set name from end of url if name is empty
                _name = _url.rsplit("/", 1)[-1]
                repo.name.set(_name)

            _repos.append({
                "name": _name,
                "url": _url,
            })

        self.settings["repositories"] = _repos
        self.settings["email"] = self.email_entry.email.get()
        with open(target, mode="w", encoding="utf-8") as f:
            json.dump(self.settings, f, allow_nan=False)

    def delete_row(self) -> Callable[[Any], None]:
        # Delete row that is pressed button
        def _delete(event: Any) -> None:
            self.repos.remove(event.widget.master)
            event.widget.master.destroy()

        return _delete

    def run(self) -> None:
        self.root = tkinter.Tk()
        self.root.title("Edit settings")
        self.root.minsize(width=400, height=0)

        # Add and Save button
        self.button = Buttons(self.root, self.load_setting,
                              self.add_row, self.save_json)

        # Email Entry
        self.email_entry = EmailEntry(self.root)

        # Entry labels
        Labels(self.root)

        self.root.mainloop()

    def load_setting(self) -> None:
        target = self.button.target.get()
        with open(target, mode="r", encoding="utf-8") as f:
            self.settings = json.load(f)

        self.email_entry.email.set(self.settings.get("email", "example@email.co.jp"))

        for setting in self.settings.get("repositories", []):
            _entry = RepoEntry(self.root, self.delete_row)
            _entry.url.set(setting["url"])
            _entry.name.set(setting["name"])
            self.repos.append(_entry)


if __name__ == "__main__":
    Main().run()
