import flask as Flask
from flask import Flask, messagebox


BG = "#d9f3f7"
SIDEBAR = "#28bcd4"
BTN = "#72e0dc"
BTN_DARK = "#37c6d7"
TEXT = "#222222"


class BugTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bug Tracker")
        self.geometry("1280x720")
        self.minsize(1100, 650)
        self.configure(bg=BG)

        self.current_role = tk.StringVar(value="Admin")

        self.container = tk.Frame(self, bg=BG)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (LoginPage, SignUpPage, DashboardPage, AdminDashboardPage,
                  ProjectsPage, SettingsPage, BugDetailsPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()
        if hasattr(frame, "refresh"):
            frame.refresh()


class BasePage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app

    def make_sidebar(self, active=None):
        sidebar = tk.Frame(self, bg=SIDEBAR, width=170)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="Bug Tracker", bg=SIDEBAR, fg="white",
                 font=("Arial", 12, "bold")).pack(pady=12)

        buttons = [
            ("Dashboard", DashboardPage),
            ("Projects", ProjectsPage),
            ("Settings", SettingsPage),
            ("Admin", AdminDashboardPage),
            ("Log out", LoginPage),
        ]

        for text, page in buttons:
            btn = tk.Button(
                sidebar, text=text, bg=BTN, fg=TEXT, relief="flat",
                command=lambda p=page: self.app.show_frame(p),
                width=14, height=1
            )
            btn.pack(pady=18 if text != "Dashboard" else 20)

        return sidebar


class LoginPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        center = tk.Frame(self, bg=BG)
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="BUG TRACKER", bg=BG, fg=TEXT,
                 font=("Arial", 26, "bold")).pack(pady=15)

        tk.Label(center, text="Username", bg=BG, fg=TEXT,
                 font=("Arial", 11)).pack(anchor="w")
        self.username = tk.Entry(center, width=32, font=("Arial", 12))
        self.username.pack(pady=6)

        tk.Label(center, text="Password", bg=BG, fg=TEXT,
                 font=("Arial", 11)).pack(anchor="w")
        self.password = tk.Entry(center, width=32, font=("Arial", 12), show="*")
        self.password.pack(pady=6)

        role_frame = tk.Frame(center, bg=BG)
        role_frame.pack(pady=8, fill="x")
        tk.Label(role_frame, text="Role", bg=BG, fg=TEXT).pack(side="left")
        role = ttk.Combobox(role_frame, textvariable=self.app.current_role,
                            values=["Admin", "Developer", "Project Manager"],
                            state="readonly", width=18)
        role.pack(side="left", padx=10)

        tk.Button(center, text="Login", bg=BTN_DARK, fg=TEXT, relief="flat",
                  width=12, command=self.login).pack(pady=12)

        tk.Button(center, text="Don't have an account? Sign Up",
                  bg=BG, fg="blue", relief="flat",
                  command=lambda: self.app.show_frame(SignUpPage)).pack(pady=5)

    def login(self):
        role = self.app.current_role.get()
        if role == "Admin":
            self.app.show_frame(AdminDashboardPage)
        else:
            self.app.show_frame(DashboardPage)


class SignUpPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        form = tk.Frame(self, bg=BG)
        form.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(form, text="Create Account", bg=BG, fg=TEXT,
                 font=("Arial", 24, "bold")).pack(pady=10)

        self.entries = {}
        fields = ["Username", "Password", "First name", "Last name", "Email", "Date of birth"]
        for field in fields:
            tk.Label(form, text=field, bg=BG, fg=TEXT).pack(anchor="w")
            e = tk.Entry(form, width=36, font=("Arial", 11))
            e.pack(pady=5)
            self.entries[field] = e

        tk.Label(form, text="Role", bg=BG, fg=TEXT).pack(anchor="w")
        self.role = ttk.Combobox(form, values=["Developer", "Project Manager"], state="readonly")
        self.role.set("Developer")
        self.role.pack(pady=5, fill="x")

        btns = tk.Frame(form, bg=BG)
        btns.pack(pady=12)
        tk.Button(btns, text="Sign Up", bg=BTN_DARK, fg=TEXT, relief="flat",
                  width=12, command=self.signup).pack(side="left", padx=8)
        tk.Button(btns, text="Back", bg=BTN, fg=TEXT, relief="flat",
                  width=12, command=lambda: self.app.show_frame(LoginPage)).pack(side="left", padx=8)

    def signup(self):
        messagebox.showinfo("Success", "Account created successfully.")
        self.app.show_frame(LoginPage)


class DashboardPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.make_sidebar()

        main = tk.Frame(self, bg=BG)
        main.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        tk.Label(main, text="What do you want to do?", bg=BG, fg=TEXT,
                 font=("Arial", 18, "bold")).pack(anchor="w", pady=10)

        for txt, cmd in [
            ("Change Username", self.change_username),
            ("Change Password", self.change_password),
            ("Change Email", self.change_email),
        ]:
            tk.Button(main, text=txt, bg=BTN, fg=TEXT, relief="flat",
                      width=20, height=2, command=cmd).pack(anchor="w", pady=12)

    def change_username(self):
        messagebox.showinfo("Settings", "Change username clicked.")

    def change_password(self):
        messagebox.showinfo("Settings", "Change password clicked.")

    def change_email(self):
        messagebox.showinfo("Settings", "Change email clicked.")


class AdminDashboardPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.make_sidebar(active="Admin")

        left = tk.Frame(self, bg=SIDEBAR, width=170)
        left.pack(side="left", fill="y")

        # Replace sidebar with admin actions
        for widget in left.winfo_children():
            widget.destroy()

        tk.Label(left, text="Admin Dashboard", bg=SIDEBAR, fg="white",
                 font=("Arial", 12, "bold")).pack(pady=12)

        for txt in ["Add", "Edit", "Remove", "Log Out"]:
            tk.Button(left, text=txt, bg=BTN, fg=TEXT, relief="flat",
                      width=14, height=1,
                      command=lambda t=txt: self.action(t)).pack(pady=18)

        right = tk.Frame(self, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        nb = ttk.Notebook(right)
        nb.pack(fill="both", expand=True, padx=8, pady=8)

        self.personnel_tab = tk.Frame(nb, bg=BG)
        self.projects_tab = tk.Frame(nb, bg=BG)
        nb.add(self.personnel_tab, text="Personnel")
        nb.add(self.projects_tab, text="Projects")

        self.setup_personnel_table()
        self.setup_projects_table()

    def action(self, text):
        if text == "Log Out":
            self.app.show_frame(LoginPage)
        else:
            messagebox.showinfo("Admin", f"{text} clicked.")

    def setup_personnel_table(self):
        columns = ("Type", "Username", "Password", "First name", "Last name", "Email", "Date of birth", "Projects")
        tree = ttk.Treeview(self.personnel_tab, columns=columns, show="headings")
        for c in columns:
            tree.heading(c, text=c)
            tree.column(c, width=120, anchor="w")

        sample = [
            ("Developer", "mohammed", "12345", "Mohammed", "yousef", "mohammedyous..." , "7/5/2000", "Bug Tracker"),
            ("Developer", "ahmed", "12345", "Ahmed", "Yousef", "ahmedyousef@...", "9/1/2003", "Bug Tracker"),
            ("Developer", "ziad", "12345", "Ziad", "Ashraf", "ziadAshraf@g...", "9/3/2001", "Bug Tracker"),
            ("Project Manager", "yousefktp", "yousef123", "Yousef", "Kotp", "yousef@gmail.com", "4/2/2002", ""),
            ("Project Manager", "marwan", "marwan", "Marwan", "Hassan", "maromaro@gmail.com", "12/17/1997", ""),
        ]
        for row in sample:
            tree.insert("", "end", values=row)

        tree.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_projects_table(self):
        columns = ("Title", "Description", "Project Manager", "Date Started", "Deadline", "Done?")
        tree = ttk.Treeview(self.projects_tab, columns=columns, show="headings")
        for c in columns:
            tree.heading(c, text=c)
            tree.column(c, width=170, anchor="w")

        tree.insert("", "end", values=(
            "Bug Tracker",
            "A bug tracker is a software which takes each and every bug related to the project which the team work on",
            "yousefkotp",
            "26-09-2021",
            "9/30/2021",
            "NO"
        ))
        tree.pack(fill="both", expand=True, padx=10, pady=10)


class ProjectsPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.make_sidebar()

        main = tk.Frame(self, bg=BG)
        main.pack(side="left", fill="both", expand=True)

        tk.Label(main, text="Projects", bg=BG, fg=TEXT,
                 font=("Arial", 18, "bold")).pack(anchor="w", padx=20, pady=10)

        cols = ("Title", "Description", "Manager", "Start Date", "Deadline", "Done?")
        tree = ttk.Treeview(main, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=160, anchor="w")

        tree.insert("", "end", values=(
            "Bug Tracker",
            "A bug tracker is a software which takes each and every bug related to the project...",
            "yousefkotp",
            "26-09-2021",
            "9/30/2021",
            "NO"
        ))
        tree.pack(fill="both", expand=True, padx=20, pady=20)


class SettingsPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.make_sidebar()

        main = tk.Frame(self, bg=BG)
        main.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        tk.Label(main, text="What do you want to do?", bg=BG, fg=TEXT,
                 font=("Arial", 18, "bold")).pack(anchor="w", pady=10)

        for txt in ["Change Username", "Change Password", "Change Email"]:
            tk.Button(main, text=txt, bg=BTN, fg=TEXT, relief="flat",
                      width=20, height=2,
                      command=lambda t=txt: messagebox.showinfo("Settings", t)).pack(anchor="w", pady=12)


class BugDetailsPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True, padx=15, pady=15)

        top = tk.Frame(main, bg=BG)
        top.pack(fill="x")

        tk.Label(top, text="Title: Screenshot feature is not working",
                 bg=BG, fg=TEXT, font=("Arial", 18, "bold")).pack(anchor="w", pady=4)

        right = tk.Frame(top, bg=BG)
        right.pack(anchor="e")

        tk.Label(right, text="Severity: Severe", bg=BG, fg=TEXT, font=("Arial", 14, "bold")).pack(anchor="e")
        tk.Label(right, text="Priority: Q1", bg=BG, fg=TEXT, font=("Arial", 14, "bold")).pack(anchor="e")
        tk.Label(right, text="Submitted By: yousefkotp", bg=BG, fg=TEXT, font=("Arial", 14, "bold")).pack(anchor="e")
        tk.Label(right, text="Date Of Submission: 2021-09-26", bg=BG, fg=TEXT, font=("Arial", 14, "bold")).pack(anchor="e")

        tk.Label(main, text="Description: this bug is slowing our progress and it has...",
                 bg=BG, fg=TEXT, font=("Arial", 16)).pack(anchor="w", pady=25)

        bottom = tk.Frame(main, bg=BG)
        bottom.pack(side="bottom", fill="x", pady=20)

        tk.Label(bottom, text="Comments:", bg=BG, fg=TEXT, font=("Arial", 16, "bold")).pack(side="left")
        comment_box = tk.Text(bottom, width=20, height=6)
        comment_box.pack(side="left", padx=20)

        tk.Button(bottom, text="Add Comment", bg=BTN, fg=TEXT, relief="flat",
                  command=lambda: messagebox.showinfo("Comment", "Comment added.")).pack(side="left", padx=5)

        tk.Button(bottom, text="Done?", bg=BTN, fg=TEXT, relief="flat",
                  command=lambda: messagebox.showinfo("Status", "Marked as done.")).pack(side="right", padx=8)
        tk.Button(bottom, text="Cancel", bg=BTN, fg=TEXT, relief="flat",
                  command=lambda: self.app.show_frame(ProjectsPage)).pack(side="right", padx=8)


if __name__ == "__main__":
    app = BugTrackerApp()
    app.mainloop()