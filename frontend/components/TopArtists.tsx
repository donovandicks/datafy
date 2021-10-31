import { Box, Button, Card, CardHeader, Menu, MenuItem } from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { useEffect, useState } from 'react';

const baseUrl = 'http://localhost:5000';

const dateRanges = ['This month', 'Last 6 months', 'Last 3 years'];

const dateToTerm: { [key: string]: string } = {
  'This month': 'short_term',
  'Last 6 months': 'medium_term',
  'Last 3 years': 'long_term',
}

interface ArtistRow {
  id: number,
  artist: string,
}

const columns: GridColDef[] = [
  { field: 'id', headerName: 'Rank', width: 100 },
  { field: 'artist', headerName: 'Artists', width: 700 },
];

const retrieveData = async (date: string) => {
  const newRows = await fetch(`${baseUrl}/artists?time_range=${dateToTerm[date]}`, {
    mode: 'cors'
  })
    .then(res => res.json())
    .then((result) => {
      return (result.map((res: any, idx: number) => ({
        id: idx + 1,
        artist: res,
      })));
    });

  return newRows;
}

const TopArtists = () => {
  const [rows, setRows] = useState<ArtistRow[]>([]);
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedDate, setDate] = useState<string>('This month');

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  }

  const handleClose = async (date: string) => {
    if (date !== selectedDate) {
      setDate(date);
      setRows(await retrieveData(date));
    }
    setAnchorEl(null);
  }

  useEffect(() => {
    fetch(`${baseUrl}/artists?time_range=short_term`, {
      mode: 'cors'
    })
      .then(res => res.json())
      .then((result) => {
        setRows(result.map((res: any, idx: number) => ({
          id: idx + 1,
          artist: res,
        })));
      }, (_) => setRows([]))
  }, []);

  return (
    <Card>
      <CardHeader 
        action={
          <div>
            <Button
              // className={classes.headerButton}
              size="small"
              variant="text"
              aria-controls="simple-menu"
              aria-haspopup="true"
              onClick={handleClick}
            >
              {selectedDate}
            </Button>
            <Menu
              id="simple-menu"
              anchorEl={anchorEl}
              keepMounted
              open={Boolean(anchorEl)}
              onClose={() => handleClose(selectedDate)}
            >
              {dateRanges.map((date) => (
                <MenuItem key={date} onClick={() => handleClose(date)}>
                  {date}
                </MenuItem>
              ))}
            </Menu>
          </div>
        }
        title='Top Artists'
      />
      <Box sx={{ minWidth: 800 }}>
        <div style={{ height: 540, width: '100%' }}>
          <DataGrid
            rows={rows}
            columns={columns}
            pageSize={10}
            rowsPerPageOptions={[10]}
          />
        </div>
      </Box>
    </Card>
  );
};

export default TopArtists;