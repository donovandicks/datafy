import { Box, Container, Grid, Paper } from '@mui/material';
import { experimentalStyled as styled } from '@mui/material/styles';
import * as React from 'react';
import TopArtists from './TopArtists';
import TopTracks from './TopTracks';
import TracksByGenre from './TracksByGenre';

const Item = styled(Paper)(({ theme }) => ({
  ...theme.typography.body2,
  padding: theme.spacing(2),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));

export default function Dashboard() {
  return (
    <Box sx={{
      backgroundColor: 'background.default',
      minHeight: '100%'
    }}>
      <Container maxWidth={false}>
        <Grid
          container
          spacing={3}
        >
          <Grid
            item
            lg={8}
            md={12}
            xl={8}
            xs={12}
          >
            <TopTracks />
          </Grid>
          <Grid
            item
            lg={8}
            md={12}
            xl={8}
            xs={12}
          >
            <TopArtists />
          </Grid>
          <Grid
            item
            lg={4}
            md={6}
            xl={4}
            xs={12}
          >
            <TracksByGenre />
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}