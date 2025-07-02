import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import * as Papa from 'papaparse';
import { map, Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ZoneDataService {
  constructor(private http: HttpClient) {}

  getZones(): Observable<any[]> {
    return this.http.get('assets/taxi_zone_lookup.csv', { responseType: 'text' }).pipe(
      map(csv => {
        const parsed = Papa.parse(csv, {
          header: true,
          skipEmptyLines: true
        });
        return parsed.data;
      })
    );
  }
}
