import { Box, Card, CardHeader } from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { useEffect, useState } from 'react';

const columns: GridColDef[] = [
  { field: 'id', headerName: 'Rank', width: 100 },
  { field: 'song', headerName: 'Song', width: 300 },
  { field: 'artist', headerName: 'Artists', width: 400 },
];

const TopTracks = () => {
  const [rows, setRows] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/toptracks', {
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
      <CardHeader title='Top Played' />
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