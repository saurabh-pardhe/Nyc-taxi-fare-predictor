import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ZoneDataService } from './zone-dataservice';
@Component({
  selector: 'app-predictorcomponent',
  standalone: false,
  templateUrl: './predictorcomponent.html',
  styleUrl: './predictorcomponent.scss'
})
export class Predictorcomponent {
  pickup: number = 0;
  dropoff: number = 0;
  passengers: number = 1;
  prediction: string | null = null;
  locations: any[] = [];

  constructor(private http: HttpClient,private zoneService: ZoneDataService ) {}
//new code
ngOnInit(): void {
  this.zoneService.getZones().subscribe(
    (data: any[]) => {
      console.log('Loaded zones:', data);
      this.locations = data;
    },
    (error: any) => {
      console.error('Failed to load zones:', error);
    }
  );
}


//
  predictFare() {
    const pickupName = this.getZoneName(this.pickup);
    const dropoffName = this.getZoneName(this.dropoff);
    const inputData = {
      pickupLocationId: Number(this.pickup),
      DroplocationId: Number(this.dropoff),
      numOfPassengers: Number(this.passengers),
      pickupLocationName: pickupName,
      dropLocationName: dropoffName

    };

    this.http.post<any>('http://localhost:8000/predict', inputData).subscribe({
      next: (res) => {
        this.prediction = res.prediction[0];
      },
      error: (err) => {
        console.error(err);
        this.prediction = 'Error predicting fare.';
      }
    });
  }
  getZoneName(id: number): string {
    const loc = this.locations.find(zone => zone.LocationID === id);
    return loc ? loc.Zone : '';
  }

}
