use aoc_client::{AocClient, AocResult};
use crate::year2022::day1::part2;
use std::path::Path;

pub mod year2022;

fn main() -> AocResult<()> {
    let client = AocClient::builder()
        .session_cookie_from_file(Path::new("C:/Users/Tom/.config/aocd/token"))?
        .year(2022)?
        .day(1)?
        .build()?;

    let data: String = client.get_input()?;

    let result = part2(data);
    println!("{}", result);

    Ok(())
}
