import { Box, Card, CardContent, CardHeader, colors, Divider } from '@mui/material';
import { Doughnut } from 'react-chartjs-2';

export default function TracksByGenre() {
  const data = {
    datasets: [
      {
        data: [63, 15, 22],
        backgroundColor: [
          colors.indigo[500],
          colors.red[600],
          colors.orange[600]
        ],
        borderWidth: 8,
        borderColor: colors.common.white,
        hoverBorderColor: colors.common.white
      }
    ],
    labels: ['Rap', 'Jazz', 'R&B']
  };

  return (
    <Card>
      <CardHeader title='Tracks By Genre' />
      <Divider />
      <CardContent>
        <Box
          sx={{
            height: 500,
            position: 'relative'
          }}
        >
          <Doughnut
            data={data}
          />
        </Box>
      </CardContent>
    </Card>
  );
}