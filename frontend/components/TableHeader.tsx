import { Button, CardHeader, Menu, MenuItem } from "@mui/material";

const dateRanges = ['This month', 'Last 6 months', 'Last 3 years'];

interface TableHeaderProps {
  title: string, 
  selectedDate: string,
  anchorEl: any,
  handleClose: (date: string) => void,
  handleClick: (event) => void,
}

const TableHeader = (props: TableHeaderProps) => {
  return (
    <CardHeader
      action={
        <div>
          <Button
            // className={classes.headerButton}
            size="small"
            variant="text"
            aria-controls="simple-menu"
            aria-haspopup="true"
            onClick={props.handleClick}
          >
            {props.selectedDate}
          </Button>
          <Menu
            id="simple-menu"
            anchorEl={props.anchorEl}
            keepMounted
            open={Boolean(props.anchorEl)}
            onClose={() => props.handleClose(props.selectedDate)}
          >
            {dateRanges.map((date) => (
              <MenuItem key={date} onClick={() => props.handleClose(date)}>
                {date}
              </MenuItem>
            ))}
          </Menu>
        </div>
      }
      title={props.title}
    />
  );
}

export default TableHeader;