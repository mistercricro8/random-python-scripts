import itertools
import json

HOURS = 15
DAYS = 5


def create_mat(comb):
    mat = [[0] * DAYS for _ in range(HOURS)]

    for _, times in comb:
        for day, start, end in times:
            for hour in range(start, end):
                if mat[hour][day] == 1:
                    return None
                mat[hour][day] = 1

    return mat


def get_inactives(mat):
    count = 0

    for day in range(DAYS):
        start, end = -1, -1
        for hour in range(HOURS):
            if mat[hour][day] == 1:
                if start == -1:
                    start = hour
                end = hour

        if start != -1 and end != -1:
            actives = sum(mat[hour][day] for hour in range(start, end + 1))
            count += (end - start + 1) - actives

    return count


def get_best(courses):
    combs = itertools.product(*(course["times"].items() for course in courses))

    best_comb = None
    min_inactive = float("inf")

    for comb in combs:
        mat = create_mat(comb)
        if mat is None:
            continue

        inactive = get_inactives(mat)

        if inactive < min_inactive:
            min_inactive = inactive
            best_comb = comb

    best_comb_format = [
        {"course": courses[i]["name"], "group": group, "times": times}
        for i, (group, times) in enumerate(best_comb)
    ]

    return best_comb_format, min_inactive


if __name__ == "__main__":
    with open("input.json", "r") as file:
        input_json = file.read()

    courses = json.loads(input_json)
    best_comb, min_inactive = get_best(courses)

    print("best:")
    for item in best_comb:
        print(f"{item['course']}: group {item['group']}, times: {item['times']}")
    print(f"hours: {min_inactive}")
