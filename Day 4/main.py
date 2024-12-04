with open ("input.txt", "r", encoding="utf-8") as file:
    lines = [line[:-1] for line in file.readlines()]

    width = len(lines[0])
    height = len(lines)
    
    result = 0

    for j in range(height):
        for i in range(width):
            if lines[j][i] == "X":
                h = lines[j][i:i+4]
                if h == "XMAS":
                    result += 1
                reverse_h = lines[j][i-3:i+1]
                if reverse_h == "SAMX":
                    result += 1

                if j+3 < height:
                    v = lines[j][i] + lines[j+1][i] + lines[j+2][i] + lines[j+3][i]
                    if v == "XMAS":
                        result += 1
                

                if j - 3 >= 0:
                    reverse_v = lines[j][i] + lines[j-1][i] + lines[j-2][i] + lines[j-3][i]
                    if reverse_v == "XMAS":
                        result += 1

                if j+3 < height and i+3 < width:
                    right_d = lines[j][i] + lines[j+1][i+1] + lines[j+2][i+2] + lines[j+3][i+3]
                    if right_d == "XMAS":
                        result += 1

                if j-3 >= 0 and i-3 >= 0:
                    reverse_right_d = lines[j][i] + lines[j-1][i-1] + lines[j-2][i-2] + lines[j-3][i-3]
                    if reverse_right_d == "XMAS":
                        result += 1

                if j+3 < height and i-3 >= 0:
                    left_d = lines[j][i] + lines[j+1][i-1] + lines[j+2][i-2] + lines[j+3][i-3]
                    if left_d == "XMAS":
                        result += 1

                if j-3 >= 0 and i+3 < width:
                    reverse_left_d = lines[j][i] + lines[j-1][i+1] + lines[j-2][i+2] + lines[j-3][i+3]
                    if reverse_left_d == "XMAS":
                        result += 1

    print("[Part1] Total is", result)

    result_2 = 0

    for j in range(height):
        for i in range(width):
            if lines[j][i] == "A" and 1 <= j and j < height - 1 and 1 <= i and i < width - 1:
                right_d = lines[j-1][i-1] + lines[j][i] + lines[j+1][i+1]
                left_d = lines[j-1][i+1] + lines[j][i] + lines[j+1][i-1]

                if right_d in ["MAS", "SAM"] and left_d in ["MAS", "SAM"]:
                    result_2 += 1

    print("[Part2] Total is", result_2)
