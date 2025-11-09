import random
import time
import statistics
import xlsxwriter
from sorting_algorithms import (
    bubble_sort,
    insertion_sort,
    selection_sort,
    gnome_sort,
    quick_sort,
    shell_sort,
    merge_sort
)

ALGORITHMS = {
    "Бульбашкове": bubble_sort,
    "Вставками": insertion_sort,
    "Вибором": selection_sort,
    "Гном'яче": gnome_sort,
    "Швидке": quick_sort,
    "Шелла": shell_sort,
    "Злиттям": merge_sort
}

# Розміри масивів
SIZES = [1111, 4444, 7777, 11111, 13333, 16666, 22222, 33333]
REPEATS = 3


def measure_time(sort_func, data):
    arr = data.copy()
    start = time.perf_counter()
    sort_func(arr)
    end = time.perf_counter()
    return end - start


def main():
    results = {name: [] for name in ALGORITHMS}

    for size in SIZES:
        print(f"\n{'=' * 80}")
        print(f"Тестування масиву розміром {size} елементів")
        print(f"{'=' * 80}")

        datasets = [
            [random.randint(0, 10**6) for _ in range(size)]
            for _ in range(REPEATS)
        ]

        for name, func in ALGORITHMS.items():
            times = []
            print(f"\n{name} сортування:")

            for i, data in enumerate(datasets, start=1):
                t = measure_time(func, data)
                print(f"   {name} сортування #{i} масиву – {t:.4f} с")
                times.append(t)

            avg_time = statistics.mean(times)
            results[name].append(avg_time)
            print(f"   ➤ Середній час: {avg_time:.4f} с")

    # Таблиця
    print("\n" + "=" * 80)
    print(f"{'Алгоритм':<15} | " + " | ".join(f"{size:>8}" for size in SIZES))
    print("-" * 80)
    for name, times in results.items():
        print(f"{name:<15} | " + " | ".join(f"{t:8.3f}" for t in times))
    print("=" * 80)

    workbook = xlsxwriter.Workbook("sorting_results.xlsx")
    worksheet = workbook.add_worksheet("Результати")

    bold = workbook.add_format({"bold": True, "bg_color": "#D9E1F2"})
    num_format = workbook.add_format({"num_format": "0.000"})

    worksheet.write(0, 0, "Алгоритм", bold)
    for col, size in enumerate(SIZES, start=1):
        worksheet.write(0, col, f"{size} елементів", bold)

    for row, (name, times) in enumerate(results.items(), start=1):
        worksheet.write(row, 0, name)
        for col, t in enumerate(times, start=1):
            worksheet.write_number(row, col, t, num_format)

    workbook.close()
    print("\n✅ Результати збережено у файлі: sorting_results.xlsx")


if __name__ == "__main__":
    main()
