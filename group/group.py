#!/usr/bin/env python3
# -*- coding=utf-8 -*-

try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import os
import re
import shutil
import subprocess
import sys
from tkinter import *
from tkinter import filedialog, ttk
import zipfile

import jieba
from nltk.tokenize import sent_tokenize, word_tokenize

from zhon_hanzi import sentence as zh_sent_re
zh_sent_compiled_re = re.compile(zh_sent_re)

cwd = os.path.dirname(os.path.abspath(__file__))
existing_nltk_data = os.environ.get("NLTK_DATA", "")
os.environ["NLTK_DATA"] = f"{cwd}{os.pathsep}{existing_nltk_data}"

DOCX_NAMESPACE = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
DOCX_PARA = DOCX_NAMESPACE + "p"
DOCX_TEXT = DOCX_NAMESPACE + "t"

def read_docx(path: str) -> str:
    """
    Take the path of a docx file as argument, return the text in unicode.
    This approach does not extract text from headers and footers.

    https://etienned.github.io/posts/extract-text-from-word-docx-simply/
    """
    with zipfile.ZipFile(path) as zip_file:
        xml_content = zip_file.read("word/document.xml")
    tree = XML(xml_content)

    paragraphs = []
    for paragraph in tree.iter(DOCX_PARA):
        text = "".join(node.text for node in paragraph.iter(DOCX_TEXT) if node.text)
        paragraphs.append(text)
    return "\n".join(paragraphs)


def read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return content

def tokenize_sent_en(s:str) -> list[str]:
    return sent_tokenize(s)

def tokenize_sent_zh(s:str) -> list[str]:
    return zh_sent_compiled_re.findall(s)

def tokenize_word_en(s:str) -> list[str]:
    return word_tokenize(s)

def tokenize_word_zh(s:str) -> list[str]:
    return list(jieba.cut(s))

def process_file(file_path):
    if not file_path:
        return
    is_ignore_punctuation = ignore_punctuation_var.get()
    write_to_log(f"Processing {file_path}...")

    ext = os.path.splitext(file_path)[-1]
    if ext == ".docx":
        content = read_docx(file_path)
    elif ext == ".txt":
        content = read_txt(file_path)
    else:
        write_to_log(f"Unsupported filetype: {ext}. Skipped.")
        return

    language = langvar.get()
    sentences = sent_tokenize_mapping[language](content)

    length_sentence_mapping = {}
    for sentence in sentences:
        tokens = word_tokenize_mapping[language](sentence)
        if is_ignore_punctuation:
            tokens = [t for t in tokens if t.isalnum()]
        length = len(tokens)
        if length in length_sentence_mapping:
            length_sentence_mapping[length].append(" ".join(tokens))
        else:
            length_sentence_mapping[length] = [" ".join(tokens)]
    basename = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.join(desktop, "counting_result", basename)
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    for length, sentences in length_sentence_mapping.items():
        output_file = os.path.join(output_dir, str(length) + ".txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(sentences))
    write_to_log(f"Results have been saved to {output_dir}.")


def process_folder(folder_path):
    if folder_path:
        write_to_log(f"Processing folder: {folder_path}")
        text_files = [f for f in os.listdir(folder_path) if (f.endswith(".txt") or f.endswith(".docx"))]
        if not text_files:
            write_to_log("No text files found in the selected folder.")
            return
        for file_name in text_files:
            file_path = os.path.join(folder_path, file_name)
            process_file(file_path)
        write_to_log("Done.")


# Configure logging
def write_to_log(msg):
    log_console["state"] = "normal"
    if log_console.index("end-1c") != "1.0":
        log_console.insert("end", "\n")
    log_console.insert("end", msg)
    log_console["state"] = "disabled"

def start_gui(*, with_restart_button:bool=False):
    global root
    root = Tk()
    root.title("Group Sentences by Length")
    mainframe = ttk.Frame(root)
    mainframe.grid(column=0, row=0, sticky="nswe")

    style = ttk.Style()
    style.theme_use("alt")

    process_file_button = ttk.Button(
        mainframe, text="Process File", command=lambda: process_file(filedialog.askopenfilename())
    )
    process_file_button.grid(column=2, row=2, sticky="w")

    process_folder_button = ttk.Button(
        mainframe, text="Process Folder", command=lambda: process_folder(filedialog.askdirectory())
    )
    process_folder_button.grid(column=3, row=2, sticky="w")

    ttk.Label(mainframe, text="Language:").grid(column=1, row=1, sticky="se")
    global langvar
    langvar = StringVar()
    lang = ttk.Combobox(mainframe, textvariable=langvar)
    lang['values'] = ('Chinese', 'English')
    lang.set("Chinese")
    lang.state(["readonly"]) # only predefined values are allowed, users cannot enter their own
    lang.grid(column=2, row=1, sticky="sw")
    global sent_tokenize_mapping
    sent_tokenize_mapping = {"Chinese": tokenize_sent_zh, "English": tokenize_sent_en}
    global word_tokenize_mapping
    word_tokenize_mapping = {"Chinese": tokenize_word_zh, "English": tokenize_word_en}

    # Checkbox to ignore punctuation marks
    global ignore_punctuation_var
    ignore_punctuation_var = BooleanVar()
    ignore_punctuation_checkbox = ttk.Checkbutton(
        mainframe, text="Ignore Punctuation Marks", variable=ignore_punctuation_var
    )
    ignore_punctuation_checkbox.grid(column=3, row=1, sticky="sw")

    global log_console
    log_console = Text(mainframe, state="disabled", width=80, height=24, wrap="none")
    log_console.grid(column=1, row=3, columnspan=5, sticky="nswe")

    if with_restart_button:
        # for tuning and debugging
        ttk.Button(mainframe, text="Restart", command=restart).grid(column=3, row=4, sticky="sw")
        ttk.Button(mainframe, text="Quit", command=lambda :root.destroy()).grid(column=4, row=4, sticky="sw")

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()

def restart(*args):
    root.destroy()

    args = [sys.executable] + sys.argv
    env = os.environ.copy()
    # If close_fds is true, all file descriptors except 0, 1 and 2 will be
    # closed before the child process is executed. Otherwise when close_fds is
    # false, file descriptors obey their inheritable flag as described in
    # Inheritance of File Descriptors
    subprocess.call(args, env=env, close_fds=False)

desktop = os.path.normpath(os.path.expanduser("~/Desktop"))
start_gui(with_restart_button=False)
