import { Box, Card, CardHeader } from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';

const columns: GridColDef[] = [
  { field: 'id', headerName: 'Rank', width: 100 },
  { field: 'song', headerName: 'Song', width: 300 },
  { field: 'artist', headerName: 'Artist', width: 400 },
];

const rows = [
  { id: 1, song: 'PTSD', artist: 'JPEGMAFIA' },
];

export default function TopTracks() {
  return (
    <Card>
      <CardHeader title='Top Played' />
      <Box sx={{ minWidth: 800 }}>
        <div style={{ height: 400, width: '100%' }}>
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