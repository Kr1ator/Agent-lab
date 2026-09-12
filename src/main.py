from src.llm import ask_llm


def main() -> None:
    user_input = input("You: ") # 在终端显示 You: ，暂停程序，等用户键盘输入；用户按回车后，把输入内容作为字符串保存到 user_input。
    try:
        result = ask_llm(user_input)
    except RuntimeError as exc:
        print(f"Error: {exc}")
        return

    print("\n--- Agent Response ---")
    print(f"Intent: {result.intent}")
    print(f"Answer: {result.answer}")
    print(f"Confidence: {result.confidence}")


if __name__ == "__main__":
    main()