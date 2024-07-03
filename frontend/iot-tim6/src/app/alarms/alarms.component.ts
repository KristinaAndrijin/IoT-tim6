// alarms.component.ts

import { Component, OnInit } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { AlarmsService } from '../alarms.service';

@Component({
  selector: 'app-alarms',
  templateUrl: './alarms.component.html',
  styleUrls: ['./alarms.component.css']
})
export class AlarmsComponent implements OnInit {
  isAlarmActive: boolean = true;
  pinInput: string = '';
  alarmReason: string = 'Došla uštriaaaaaaaaaaaaaa';
  isGsgAlarmActive: boolean = false;
  isRpirAlarmActive: boolean = false;
  isDsAlarmActive: boolean = false;
  isDmsAlarmActive: boolean = false;


  constructor(private socket: Socket, private service: AlarmsService) { 
    this.socket.connect();
    this.socket.on("alarms", (message: any) => {
      if (message['type'].includes('ds')) {
        this.isDsAlarmActive = true;
      } else if (message['type'].includes('dms')) {
        this.isDmsAlarmActive = true;
      } else if (message['type'].includes('rpir')) {
        this.isRpirAlarmActive = true;
      } else if (message['type'].includes('gsg')) {
        this.isGsgAlarmActive = true;
      }
    });
  }

  ngOnInit(): void {
  }

  deactivateAlarm(pin: string): void {
    console.log('Deactivating alarm with PIN:', pin);
    this.socket.emit('turn_off_alarm', {type: "dms", pin: pin});
    this.socket.on("dms_pin", (message: any) => {
      console.log(message)
      if (message['code']) {
        this.isDmsAlarmActive = false;
        this.pinInput='';
      } else {
        alert("Wrong code!");
      }
    });
  }

  deactivateDsAlarm(): void {
    console.log("gasi ds")
    this.socket.emit('turn_off_alarm', {type: "ds"});
    this.isDsAlarmActive = false;
  }

  deactivateRpirAlarm(): void {
    console.log("gasi rpir")
    this.socket.emit('turn_off_alarm', {type: "rpir"});
    this.isRpirAlarmActive = false;
  }

  deactivateGsgAlarm(): void {
    console.log("gasi gsg")
    this.socket.emit('turn_off_alarm', {type: "gsg"});
    this.isGsgAlarmActive = false;
  }
}
