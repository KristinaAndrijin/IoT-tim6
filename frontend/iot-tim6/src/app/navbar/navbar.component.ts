import { Component, OnInit } from '@angular/core';
import { Socket } from 'ngx-socket-io';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

  alarm = false;
  constructor(private socket: Socket) {
    this.socket.on("alarm_exist", (alarms_exists: any) => {
      this.alarm = alarms_exists;
    });
   }

  ngOnInit(): void {
  }

}
