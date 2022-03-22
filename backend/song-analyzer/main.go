package main

import (
	"context"
	"fmt"
	"os"

	"github.com/jackc/pgx/v4"
)

type Track struct {
	track_id string
}

func main() {
	url := "postgres://localhost:5432/datafy"
	conn, err := pgx.Connect(context.Background(), url)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
		os.Exit(1)
	}

	defer conn.Close(context.Background())

	rows, err := conn.Query(context.Background(), `
	SELECT track.track_id
	FROM track
	LEFT JOIN track_detail
	ON track.track_id = track_detail.track_id
	`)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Query failed: %v\n", err)
		os.Exit(1)
	}

	var rowSlice []Track
	for rows.Next() {
		var track Track
		err := rows.Scan(&track.track_id)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Failed to scan row: %v\n", err)
		}
		rowSlice = append(rowSlice, track)
	}

	fmt.Println(rowSlice)
}
