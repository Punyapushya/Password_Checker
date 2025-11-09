import flet as ft
import re
from zxcvbn import zxcvbn

def main(page: ft.Page):
    page.bgcolor = "#0F172A"
    page.title = "Password Strength Checker"
    page.window_width = 500
    page.window_height = 600
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Password input state
    show_password = ft.Ref[ft.TextField]()
    password = ft.Ref[ft.TextField]()

    def is_sequential(pw):
        for i in range(len(pw) - 2):
            if ord(pw[i+1]) == ord(pw[i]) + 1 and ord(pw[i+2]) == ord(pw[i+1]) + 1:
                return True
        return False

    def is_repeating(pw):
        return bool(re.search(r"(.)\1", pw))

    def check_password_strength(e):
        pw = password.current.value

        result = zxcvbn(pw)
        score = result["score"]

        # Check 1 - Length
        if len(pw) >= 12:
            check1_text.value = "Strong passwords are 12 chars. or above"
            check1_bar.value = 1
            check1_bar.color = "green"
        else:
            check1_text.value = "Password is too short"
            check1_bar.value = 1
            check1_bar.color = "red"

        # Check 2 - Characters
        if re.search(r"[A-Z]", pw) and re.search(r"[a-z]", pw) and re.search(r"[0-9]", pw) and re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw):
            check2_text.value = "Upper, lower, number, special characters"
            check2_bar.value = 1
            check2_bar.color = "green"
        else:
            check2_text.value = "Missing character types"
            check2_bar.value = 1
            check2_bar.color = "red"

        # Check 3 - Repeat
        if is_repeating(pw):
            check3_text.value = "Repeating chars found"
            check3_bar.value = 1
            check3_bar.color = "red"
        else:
            check3_text.value = "No repetitions"
            check3_bar.value = 1
            check3_bar.color = "green"

        # Check 4 - Sequential
        if is_sequential(pw):
            check4_text.value = "Sequential pattern found"
            check4_bar.value = 1
            check4_bar.color = "red"
        else:
            check4_text.value = "No sequences"
            check4_bar.value = 1
            check4_bar.color = "green"

        page.update()

    def toggle_password_visibility(e):
        password.current.password = not password.current.password
        page.update()

    def copy_to_clipboard(e):
        page.set_clipboard(password.current.value)
        page.snack_bar = ft.SnackBar(ft.Text("Password copied!"), open=True)
        page.update()

    # Title and instructions
    title = ft.Text("Password Strength Check", size=20, weight="bold", color="white")
    subtitle = ft.Text("Type in a password and see how strong it is!", size=14, color="#94A3B8")

    # Condition bars and labels
    def build_check(title, desc):
        label = ft.Text(title, size=15, weight="bold", color="white")
        status = ft.Text(desc, size=12, color="#94A3B8")
        bar = ft.ProgressBar(width=200, height=4, value=0, color="green", bgcolor="#334155")
        return label, status, bar

    check1_label, check1_text, check1_bar = build_check("1. Length Check", "")
    check2_label, check2_text, check2_bar = build_check("2. Character Check", "")
    check3_label, check3_text, check3_bar = build_check("3. Repeat Check", "")
    check4_label, check4_text, check4_bar = build_check("4. Sequential Check", "")

    # Input area
    password_input = ft.Container(
        content=ft.Row([
            ft.IconButton(icon=ft.Icons.LOCK_OUTLINE, icon_color="white"),
            ft.TextField(ref=password,
                         hint_text="Enter password",
                         password=True,
                         bgcolor="#1E293B",
                         border_radius=10,
                         height=45,
                         color="white",
                         on_change=check_password_strength,
                         border_color="transparent"),
            ft.IconButton(icon=ft.Icons.VISIBILITY, on_click=toggle_password_visibility),
            ft.IconButton(icon=ft.Icons.CONTENT_COPY, on_click=copy_to_clipboard)
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=10,
        bgcolor="#1E293B",
        border_radius=10
    )

    # Final layout
    card = ft.Container(
        content=ft.Column([
            title,
            subtitle,
            ft.Divider(opacity=0),
            check1_label,
            check1_text,
            check1_bar,
            ft.Divider(height=10, color="transparent"),
            check2_label,
            check2_text,
            check2_bar,
            ft.Divider(height=10, color="transparent"),
            check3_label,
            check3_text,
            check3_bar,
            ft.Divider(height=10, color="transparent"),
            check4_label,
            check4_text,
            check4_bar,
            ft.Divider(height=20, color="transparent"),
            password_input
        ], spacing=5),
        padding=30,
        bgcolor="#1E293B",
        border_radius=20,
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(blur_radius=20, color="black", spread_radius=2)
    )

    page.add(card)

ft.app(target=main)
