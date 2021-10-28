import { Box, Card, CardHeader } from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { useEffect, useState } from 'react';

const columns: GridColDef[] = [
  { field: 'id', headerName: 'Rank', width: 100 },
  { field: 'artist', headerName: 'Artists', width: 700 },
];

const TopArtists = () => {
  const [rows, setRows] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/artists', {
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
      <CardHeader title='Top Artists' />
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