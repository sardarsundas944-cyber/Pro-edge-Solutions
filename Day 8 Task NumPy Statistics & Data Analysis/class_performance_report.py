import numpy as np
from pathlib import Path


STUDENT_NAMES = np.array([
    "Ayesha",
    "Hamza",
    "Zainab",
    "Usman",
    "Sara",
    "Ali",
    "Maryam",
    "Bilal",
    "Hania",
    "Talha",
])

SUBJECTS = np.array([
    "Maths",
    "Physics",
    "Chemistry",
    "Biology",
    "Computer Science",
])

MARKS = np.array([
    [88, 92, 85, 90, 95],
    [76, 81, 79, 84, 88],
    [90, 87, 91, 89, 93],
    [68, 72, 70, 74, 78],
    [82, 85, 88, 80, 89],
    [95, 90, 93, 91, 96],
    [74, 78, 80, 77, 82],
    [86, 88, 84, 87, 90],
    [70, 75, 73, 78, 80],
    [92, 94, 89, 90, 97],
])


def calculate_student_totals(marks):
    return np.sum(marks, axis=1)


def calculate_overall_total(marks):
    return np.sum(marks)


def calculate_per_student_average(marks):
    return np.mean(marks, axis=1)


def calculate_subject_averages(marks):
    return np.mean(marks, axis=0)


def calculate_class_statistics(marks):
    flat_marks = marks.flatten()
    return {
        "overall_total": np.sum(flat_marks),
        "average_marks": np.mean(flat_marks),
        "mean": np.mean(flat_marks),
        "median": np.median(flat_marks),
        "std_dev": np.std(flat_marks),
        "highest_marks": np.max(flat_marks),
        "lowest_marks": np.min(flat_marks),
        "percentiles": {
            "P25": np.percentile(flat_marks, 25),
            "P50": np.percentile(flat_marks, 50),
            "P75": np.percentile(flat_marks, 75),
            "P90": np.percentile(flat_marks, 90),
        },
    }


def find_top_student(student_names, totals):
    top_index = int(np.argmax(totals))
    return student_names[top_index], totals[top_index]


def find_lowest_student(student_names, totals):
    low_index = int(np.argmin(totals))
    return student_names[low_index], totals[low_index]


def class_performance_summary(class_average):
    if class_average >= 85:
        return "Excellent overall performance. Students are consistently scoring at a high level."
    if class_average >= 70:
        return "Good overall performance. Most students are meeting the expected academic standard."
    if class_average >= 55:
        return "Average performance. Improvement is needed in several subjects to raise the class standard."
    return "Below average performance. Targeted support and revision strategies are recommended."


def generate_svg_report(student_names, subjects, marks, output_path):
    totals = calculate_student_totals(marks)
    averages = calculate_per_student_average(marks)
    subject_averages = calculate_subject_averages(marks)
    stats = calculate_class_statistics(marks)

    top_student, top_total = find_top_student(student_names, totals)
    low_student, low_total = find_lowest_student(student_names, totals)

    chart_width = 620
    max_bar = max(subject_averages) if len(subject_averages) else 1
    x_start = 70
    y_base = 520
    bar_w = 70
    gap = 18

    bars = []
    for idx, value in enumerate(subject_averages):
        x = x_start + idx * (bar_w + gap)
        height = (value / max_bar) * 240
        y = y_base - height
        bars.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{height}" fill="#4f46e5" rx="8"/>')
        bars.append(
            f'<text x="{x + bar_w / 2}" y="{y_base + 25}" text-anchor="middle" fill="#1f2937" font-size="12">{subjects[idx]}</text>'
        )
        bars.append(
            f'<text x="{x + bar_w / 2}" y="{y - 8}" text-anchor="middle" fill="#111827" font-size="11">{value:.1f}</text>'
        )

    class_avg = stats["average_marks"]
    summary = class_performance_summary(class_avg)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="760" viewBox="0 0 1000 760">
      <rect width="100%" height="100%" fill="#f8fafc"/>
      <text x="50" y="60" font-family="Arial, sans-serif" font-size="34" font-weight="bold" fill="#111827">Class Performance Report</text>
      <text x="50" y="90" font-family="Arial, sans-serif" font-size="16" fill="#475569">Performance analysis using NumPy statistics</text>

      <text x="50" y="140" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#1f2937">Overview</text>
      <text x="50" y="170" font-family="Arial, sans-serif" font-size="15" fill="#334155">Top Student: {top_student} ({top_total} marks)</text>
      <text x="50" y="195" font-family="Arial, sans-serif" font-size="15" fill="#334155">Lowest Student: {low_student} ({low_total} marks)</text>
      <text x="50" y="220" font-family="Arial, sans-serif" font-size="15" fill="#334155">Class Average: {class_avg:.2f}</text>
      <text x="50" y="245" font-family="Arial, sans-serif" font-size="15" fill="#334155">Summary: {summary}</text>

      <text x="50" y="300" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#1f2937">Subject-wise Averages</text>
      <line x1="50" y1="520" x2="700" y2="520" stroke="#334155" stroke-width="2"/>
      <line x1="50" y1="280" x2="50" y2="520" stroke="#334155" stroke-width="2"/>
      {''.join(bars)}

      <text x="50" y="590" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#1f2937">Key Statistics</text>
      <text x="50" y="620" font-family="Arial, sans-serif" font-size="14" fill="#334155">Total Marks: {stats['overall_total']}</text>
      <text x="50" y="645" font-family="Arial, sans-serif" font-size="14" fill="#334155">Mean: {stats['mean']:.2f}</text>
      <text x="50" y="670" font-family="Arial, sans-serif" font-size="14" fill="#334155">Median: {stats['median']:.2f}</text>
      <text x="50" y="695" font-family="Arial, sans-serif" font-size="14" fill="#334155">Std Dev: {stats['std_dev']:.2f}</text>
      <text x="350" y="620" font-family="Arial, sans-serif" font-size="14" fill="#334155">Highest Marks: {stats['highest_marks']}</text>
      <text x="350" y="645" font-family="Arial, sans-serif" font-size="14" fill="#334155">Lowest Marks: {stats['lowest_marks']}</text>
      <text x="350" y="670" font-family="Arial, sans-serif" font-size="14" fill="#334155">P25: {stats['percentiles']['P25']:.2f}</text>
      <text x="350" y="695" font-family="Arial, sans-serif" font-size="14" fill="#334155">P75: {stats['percentiles']['P75']:.2f}</text>
    </svg>
    '''

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(svg, encoding="utf-8")


def display_report(student_names, subjects, marks):
    totals = calculate_student_totals(marks)
    averages = calculate_per_student_average(marks)
    subject_averages = calculate_subject_averages(marks)
    stats = calculate_class_statistics(marks)

    top_student, top_total = find_top_student(student_names, totals)
    low_student, low_total = find_lowest_student(student_names, totals)

    print("=" * 90)
    print("CLASS PERFORMANCE REPORT")
    print("=" * 90)
    print(f"Students Evaluated: {len(student_names)}")
    print(f"Subjects: {', '.join(subjects)}")
    print()

    print("Student-wise Totals and Averages")
    print("-" * 90)
    for idx, name in enumerate(student_names):
        print(f"{name:10} | Total: {totals[idx]:>3} | Average: {averages[idx]:>5.2f}")

    print()
    print("Statistical Summary")
    print("-" * 90)
    print(f"Total Marks            : {stats['overall_total']}")
    print(f"Average Marks          : {stats['average_marks']:.2f}")
    print(f"Mean                   : {stats['mean']:.2f}")
    print(f"Median                 : {stats['median']:.2f}")
    print(f"Standard Deviation     : {stats['std_dev']:.2f}")
    print(f"Highest Marks          : {stats['highest_marks']}")
    print(f"Lowest Marks           : {stats['lowest_marks']}")
    print("Percentiles            :")
    for label, value in stats["percentiles"].items():
        print(f"  {label:>3} -> {value:.2f}")

    print()
    print("Performance Insights")
    print("-" * 90)
    print(f"Top Performing Student: {top_student} with {top_total} total marks")
    print(f"Lowest Performing Student: {low_student} with {low_total} total marks")
    print("Subject-wise Average Marks:")
    for subject, avg in zip(subjects, subject_averages):
        print(f"  {subject:<18} {avg:.2f}")
    print(f"Overall Class Performance Summary: {class_performance_summary(stats['average_marks'])}")
    print("=" * 90)


def main():
    output_dir = Path(__file__).resolve().parent / "output"
    output_path = output_dir / "report_preview.svg"
    display_report(STUDENT_NAMES, SUBJECTS, MARKS)
    generate_svg_report(STUDENT_NAMES, SUBJECTS, MARKS, output_path)
    print(f"\nSVG performance chart saved to: {output_path}\n")


if __name__ == "__main__":
    main()
