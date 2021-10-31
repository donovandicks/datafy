import { Box, Card } from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { useEffect, useState } from 'react';
import TableHeader from './TableHeader';

const baseUrl = 'http://localhost:5000';

const dateToTerm: { [key: string]: string } = {
  'This month': 'short_term',
  'Last 6 months': 'medium_term',
  'Last 3 years': 'long_term',
}

interface SongRow {
  id: number,
  song: string,
  artist: string,
}

const columns: GridColDef[] = [
  { field: 'id', headerName: 'Rank', width: 100 },
  { field: 'song', headerName: 'Song', width: 300 },
  { field: 'artist', headerName: 'Artists', width: 400 },
];

const retrieveData = async (date: string) => {
  const newRows = await fetch(`${baseUrl}/songs?time_range=${dateToTerm[date]}`, {
    mode: 'cors'
  })
    .then(res => res.json())
    .then((result) => {
      return (result.map((res: any, idx: number) => ({
        id: idx + 1,
        song: res.song,
        artist: res.artists.join(', '),
      })));
    });

  return newRows;
}

const TopTracks = () => {
  const [rows, setRows] = useState<SongRow[]>([]);
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
    fetch(`${baseUrl}/songs?time_range=short_term`, {
      mode: 'cors'
    })
      .then(res => res.json())
      .then((result) => {
        setRows(result.map((res: any, idx: number) => ({
          id: idx + 1,
          song: res.song,
          artist: res.artists.join(', '),
        })));
      }, (_) => setRows([]))
  }, []);

  return (
    <Card>
      <TableHeader
        title='Top Tracks'
        selectedDate={selectedDate}
        anchorEl={anchorEl}
        handleClose={handleClose}
        handleClick={handleClick}
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

export default TopTracks;