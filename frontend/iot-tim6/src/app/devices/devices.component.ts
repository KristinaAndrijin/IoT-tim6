// devices.component.ts

import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';

@Component({
  selector: 'app-devices',
  templateUrl: './devices.component.html',
  styleUrls: ['./devices.component.css']
})
export class DevicesComponent implements OnInit {
  selectedPi: string = 'PI1';
  devicesList: any[] = [];

  piDevicesMap: any = {
    'PI1': [
      { name: 'Device 1', info: ['Info 1 - SkrapapaSkrapapaSkrapapaSkrapapaSkrapapa', 'Info 2 - Skrapapa', 'Info 3 - Skrapapa'] },
      { name: 'Device 1', info: ['Info 1'] },
      { name: 'Device 1', info: ['Info 1 - Skrapapa', 'Info 2 - Skrapapa', 'Info 3 - Skrapapa'] },
      { name: 'Device 1', info: ['Info 1 - Skrapapa', 'Info 2 - Skrapapa', 'Info 3 - Skrapapa'] },
      { name: 'Device 1', info: ['Info 1', 'Info 2', ] },
      { name: 'Device 1', info: ['Info 1', 'Info 2', 'Info 3'] },
      { name: 'Device 1', info: ['Info 1 - Skrapapa', 'Info 2 - Skrapapa', 'Info 3 - Skrapapa'] },
      { name: 'Device 1', info: ['Info 1', ] },
      { name: 'Device 1', info: ['Info 1', 'Info 2'] },
      { name: 'Device 1', info: ['Info 1', 'Info 2', 'Info 3'] },
    ],
    'PI2': [
      { name: 'Device 1', info: ['Info 1 - SkrapapaSkrapapaSkrapapaSkrapapaSkrapapa', 'Info 2 - Skrapapa', 'Info 3 - Skrapapa'] },
      { name: 'Device 2', info: ['Info 1'] },
      { name: 'Device 3', info: ['Info 1 - Skrapapa', 'Info 2 - Skrapapa', 'Info 3 - Skrapapa'] },
      { name: 'Device 4', info: ['Info 1 - Skrapapa', 'Info 2 - Skrapapa', 'Info 3 - Skrapapa'] },
    ],
    'PI3': [
      // Devices for PI3
    ],
    // Add more Raspberry Pi entries as needed
  };

  @ViewChild('grafanaIframe', { static: false }) grafanaIframe: ElementRef | undefined;

  ngOnInit(): void {
    this.updateDevicesList();
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
  


}
