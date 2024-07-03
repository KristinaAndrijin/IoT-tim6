import { Component, ElementRef, OnInit, ViewChild, OnDestroy } from '@angular/core';
import { CommsService } from '../comms.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-devices',
  templateUrl: './devices.component.html',
  styleUrls: ['./devices.component.css']
})
export class DevicesComponent implements OnInit, OnDestroy {
  selectedPi: string = 'PI1';
  devicesList: any[] = [];

  @ViewChild('grafanaIframe', { static: false }) grafanaIframe: ElementRef | undefined;

  private piDevicesSubscription: Subscription;

  constructor(private commsService: CommsService) {
    this.piDevicesSubscription = new Subscription();
  }


  ngOnInit(): void {
    this.piDevicesSubscription = this.commsService.piDevices$.subscribe(piDevices => {
      this.devicesList = piDevices[this.selectedPi] || [];
    });
    this.commsService.loadSetupFromLocalStorage(); 
    this.commsService.loadValuesFromLocalStorage();
    this.updateDevicesList();
  }
  

  ngAfterViewInit(): void {
    this.loadGrafanaDashboard();
  }

  updateDevicesList() {
    this.commsService.piDevices$.subscribe(piDevices => {
      this.devicesList = piDevices[this.selectedPi] || [];
    });
  }

  loadGrafanaDashboard() {
    if (this.grafanaIframe) {
      let grafanaLink = '';
      switch (this.selectedPi) {
        case 'PI1':
          // grafanaLink = 'http://localhost:3000/goto/cyM283cSR?orgId=1'; // Vlada
          grafanaLink = 'http://localhost:3000/goto/g5bZJDaSg?orgId=1' // Kris 
          break;
        case 'PI2':
          grafanaLink = 'http://localhost:3000/goto/RZqEajwIR?orgId=1';
          break;
        case 'PI3':
          grafanaLink = "http://localhost:3000/goto/QH5EfCQSR?orgId=1";
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

  trimValue(value: any): string {
    if (value != null) {
      return value.length > 50 ? value.slice(0, 25) + '...' : value;
    }
    return '';
  }

  ngOnDestroy(): void {
    this.piDevicesSubscription.unsubscribe();
  }
}
