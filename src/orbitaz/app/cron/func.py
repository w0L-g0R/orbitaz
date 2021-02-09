def create_text_file(content: str) -> str:
    file = open(f"copy.txt", "w")
    file.write(content)
    file.close()
    return "Created a text file"
