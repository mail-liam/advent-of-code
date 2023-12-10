fn get_totals(data: String) -> Vec<i32> {
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

    totals
}

pub fn part1(data: String) -> i32 {
    let totals = get_totals(data);

    *totals.iter().max().unwrap()
}


pub fn part2(data: String) -> i32 {
    let mut totals = get_totals(data);
    totals.sort();
    totals.reverse();

    totals[0] + totals[1] + totals[2]
}


#[cfg(test)]
mod tests {
    use super::*;

    static EXAMPLE_DATA: &str = "1000
2000
3000

4000

5000
6000

7000
8000
9000

10000";

    #[test]
    fn test_part1() {
        assert_eq!(part1(String::from(EXAMPLE_DATA)), 24000);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(String::from(EXAMPLE_DATA)), 45000);
    }
}