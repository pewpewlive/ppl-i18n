import mistake_check


def color_assert(input1: str, input2: str, expected_result: bool):
    actual_result = mistake_check.color_check(input1, input2)
    if actual_result != expected_result:
        print("Failed color check:")
        print(
            f'Expected "{expected_result}", got "{actual_result}" when checking "{input1}" with "{input2}"'
        )


def format_assert(input1: str, input2: str, expected_result: bool):
    actual_result = mistake_check.format_check(input1, input2)
    if actual_result != expected_result:
        print("Failed format check:")
        print(
            f'Expected "{expected_result}", got "{actual_result}" when checking "{input1}" with "{input2}"'
        )


def condition_assert(input1: bool, input2: bool, expected_result: str):
    actual_result = mistake_check.condition(input1, input2)
    if actual_result != expected_result:
        print("Failed condition check:")
        print(
            f'Expected "{expected_result}", got "{actual_result}" when checking "{input1}" with "{input2}"'
        )


def main():
    VALID = True
    INVALID = False

    color_assert("#ff00ffffHello!", "#ff00ffffBonjour!", VALID)
    color_assert("#ff00ffff#ffffffff!", "#ff00ffffffffffff!", INVALID)
    color_assert("#ff00ffff#ffffffff#ff00ffff", "#ff00ffff#ffffffff#ff00ffff", VALID)
    color_assert("Bonjour#ffffff!", "Labas#ffffffff!", INVALID)
    color_assert("Hello#ffffffff!", "#ffffffff!", VALID)

    format_assert("Hello %s", "Hello %s", VALID)
    format_assert("A%sB%sC%s", "X%sY%sZ%s", VALID)
    format_assert("%s world", "%s monde", VALID)
    format_assert("Hello %s", "Bonjour %S", INVALID)
    format_assert("Hello %s", "Labas $s", INVALID)
    format_assert("Hello %s", "Salut #s", INVALID)
    format_assert("Hello", "Hello %s", INVALID)
    format_assert("%1$s", "%s", INVALID)
    format_assert("Hello %1$s", "Sveiki %1$s", VALID)
    format_assert("Hello %1$s", "%1$s Bonjour", VALID)
    format_assert("Hello %1$s", "Bonjour %s", INVALID)
    format_assert("%2$s", "%2$s", VALID)
    format_assert("Hello %2$s %2$s %1$s %1$s", "Bonjour %1$s %1$s %2$s %2$s", VALID)
    format_assert("Hello %2$s %1$s %1$s", "Bonjour %1$s %1$s %1$s", INVALID)
    format_assert("Hello %1$s %2$s %3$s", "Bonjour %2$s %3$s %4$s", INVALID)

    condition_assert(False, False, "invalid_colors_and_format")
    condition_assert(True, False, "invalid_format")
    condition_assert(False, True, "invalid_colors")
    condition_assert(True, True, "")


if __name__ == "__main__":
    main()
