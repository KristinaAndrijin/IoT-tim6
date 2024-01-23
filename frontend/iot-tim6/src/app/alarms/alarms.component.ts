// alarms.component.ts

import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-alarms',
  templateUrl: './alarms.component.html',
  styleUrls: ['./alarms.component.css']
})
export class AlarmsComponent implements OnInit {
  isAlarmActive: boolean = true;
  pinInput: string = '';
  alarmReason: string = 'Došla uštriaaaaaaaaaaaaaa';
  constructor() { }

  ngOnInit(): void {
  }

  deactivateAlarm(pin: string): void {
    console.log('Deactivating alarm with PIN:', pin);
    this.isAlarmActive = false;
  }
}
