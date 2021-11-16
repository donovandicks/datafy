use dialoguer::{theme::ColorfulTheme, Confirm, Input, Select};

/// Get the query `limit` parameter from the user. The value must be within the
/// bounds of u32
///
/// # Returns
///
/// * The limit formatted as a string
pub fn get_limit() -> String {
    Input::with_theme(&ColorfulTheme::default())
        .with_prompt("Results Limit: ")
        .default(20.to_string())
        .validate_with(|input: &String| -> Result<(), &str> {
            match input.parse::<u32>() {
                Ok(_) => Ok(()),
                Err(_) => Err("Failed to parse limit. Value should be a positive integer."),
            }
        })
        .interact_text()
        .unwrap()
}

/// Get the query `time_range` parameter from the user.
///
/// The possible choices are below:
///
/// * `short_term` - the last 4 weeks
/// * `medium_term` - the last 6 months
/// * `long_term` - the last 3 years
///
/// # Returns
///
/// * The selected time_range
pub fn get_time_range() -> String {
    let choices = ["short_term", "medium_term", "long_term"];

    let index = Select::with_theme(&ColorfulTheme::default())
        .with_prompt("Time Range: ")
        .items(&choices)
        .default(1)
        .interact()
        .unwrap();

    String::from(choices[index])
}

/// Get the query `aggregate` parameter from the user
///
/// # Returns
///
/// * A string boolean
pub fn get_aggregate() -> String {
    let choices = ["true", "false"];
    let index = match Select::with_theme(&ColorfulTheme::default())
        .with_prompt("Aggregate Results: ")
        .items(&choices)
        .default(1)
        .interact()
    {
        Ok(index) => index,
        _ => panic!("Somehow received a value out of selection!"),
    };

    String::from(choices[index])
}

/// Get input item IDs from the user
///
/// # Returns
///
/// * The vector of supplied item IDs
pub fn get_item_ids(item: &str) -> Vec<String> {
    let mut items = vec![];

    if !Confirm::with_theme(&ColorfulTheme::default())
        .with_prompt(format!("Would you like to enter {} IDs?", item))
        .default(false)
        .wait_for_newline(true)
        .interact()
        .unwrap()
    {
        return items;
    }

    loop {
        let input: String = Input::with_theme(&ColorfulTheme::default())
            .with_prompt(format!("{} ID: ", item))
            .interact_text()
            .unwrap();

        items.push(input);

        if !Confirm::with_theme(&ColorfulTheme::default())
            .with_prompt(format!("Would you like to enter another {} ID?", item))
            .default(false)
            .wait_for_newline(true)
            .interact()
            .unwrap()
        {
            break;
        }
    }

    items
}
