// devices.component.ts

import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { CommsService } from '../comms.service';

@Component({
  selector: 'app-devices',
  templateUrl: './devices.component.html',
  styleUrls: ['./devices.component.css']
})
export class DevicesComponent implements OnInit {

  constructor(private commsService: CommsService) {}

  selectedPi: string = 'PI1';
  devicesList: any[] = [];

  piDevicesMap: any = {
    'PI1': [
      { name: 'Device 1', simulated: true, temperature: 30, humidity: 50 },
      { name: 'Device 2', simulated: false, temperature: 25, motionSensor: true },
      { name: 'Device 1', simulated: true, temperature: 30, humidity: 50 },
      { name: 'Device 2', simulated: false, temperature: 25, motionSensor: true },
    ],
    'PI2': [
      { name: 'Device 3', simulated: true, temperature: 28, doorSensor: true },
      { name: 'Device 4', simulated: false, temperature: 22, lightState: 'on' },
    ],
    'PI3': [
    ],
  };

  @ViewChild('grafanaIframe', { static: false }) grafanaIframe: ElementRef | undefined;


  ngOnInit(): void {
    this.updateDevicesList();
    this.commsService.connect();
    this.commsService.subscribeToTopic('angular_setup');
  }

  ngAfterViewInit(): void {
    this.loadGrafanaDashboard();
  }

  updateDevicesList() {
    this.devicesList = this.piDevicesMap[this.selectedPi];
  }

  loadGrafanaDashboard() {
    if (this.grafanaIframe) {
      let grafanaLink = '';
      switch (this.selectedPi) {
        case 'PI1':
          grafanaLink = 'http://localhost:3000/goto/cyM283cSR?orgId=1';
          break;
        case 'PI2':
          grafanaLink = 'http://localhost:3000/goto/JAydze5SR?orgId=1';
          break;
        case 'PI3':
          grafanaLink = 'http://localhost:3000/goto/GuVFzecIR?orgId=1';
          break;
      }
  
      this.grafanaIframe.nativeElement.src = grafanaLink;
    }
  }

  getDeviceInfo(device: any): { key: string, value: any }[] {
    return Object.entries(device)
      .filter(([key, value]) => key !== 'name')
      .map(([key, value]) => ({ key, value }));
  }
}
