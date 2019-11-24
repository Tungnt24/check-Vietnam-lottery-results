import bs4
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('numbers', type=str, nargs="+")
args = parser.parse_args()

jps = {
    'Giải Đặc Biệt': ['rs_0_0'],
    'Giải Nhất': ['rs_1_0'],
    "Giải Nhì": ['rs_2_0', 'rs_2_1'],
    "Giải Ba": ['rs_3_0', 'rs_3_1', 'rs_3_2', 'rs_3_3', 'rs_3_4', 'rs_3_5'],
    "Giải Tư": ['rs_4_0', 'rs_4_1', 'rs_4_2', 'rs_4_3'],
    "Giải Năm": ['rs_5_0', 'rs_5_1', 'rs_5_2', 'rs_5_5', 'rs_5_4', 'rs_5_5'],
    "Giải Sáu": ['rs_6_0', 'rs_6_1', 'rs_6_2'],
    "Giải Bảy": ['rs_7_0', 'rs_7_1', 'rs_7_2', 'rs_7_3']
}


def jackpot(numbers, lottery_results):
    result = {}
    for number in numbers:
        count = 0
        for row in lottery_results.values():
            for lottery_result in row:
                if str(number) in lottery_result[-2:]:
                    count = count + 1
        result.update({number: count})

    return result


def get_jackpot():
    r = requests.get('http://ketqua.net')
    html = bs4.BeautifulSoup(r.text, features='lxml')

    lottery_results = {}
    for name, ids in jps.items():
        results = []
        for id_ in ids:
            lottery_result = html.find('td', attrs={'id': id_}).text
            results.append(lottery_result)
        lottery_results.update({name: results})

    return lottery_results


def main():
    numbers = args.numbers
    lottery_results = jackpot(numbers, get_jackpot())
    won = False
    for number, count in lottery_results.items():
        if count != 0:
            won = True
            break

    if won:
        for number, count in lottery_results.items():
            if count == 0:
                print(f"Số {number} bạn không được nháy nào :D")
            else:
                print(f"Số {number} trúng {count} nháy")
                won = True
    elif not won:
        for name, results in get_jackpot().items():
            print(name, end=": ")
            for result in results:
                print(result, end=" ")
            print("")


if __name__ == "__main__":
    main()
