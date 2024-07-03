import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AlarmsService {

  private baseUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) { }

  turn_off_alarm(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/turn_off_alarm`, data);
  }
}
