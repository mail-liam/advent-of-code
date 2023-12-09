pub fn part1(data: String) -> i32 {
//     let data = "1000
// 2000
// 3000

// 4000

// 5000
// 6000

// 7000
// 8000
// 9000

// 10000";

    let mut totals: Vec<i32> = Vec::new();
    let mut current = 0;
    for line in data.lines() {
        if line.is_empty() {
            totals.push(current);
            current = 0;
        } else {
            current = current + line.parse::<i32>().unwrap()
        }
    }
    totals.push(current);

    *totals.iter().max().unwrap()
}