use prettytable::Row;

pub trait Content {
    fn as_row(&self, idx: &usize) -> Row;
}

pub trait ContentCollection {
    fn display(&self);
}
