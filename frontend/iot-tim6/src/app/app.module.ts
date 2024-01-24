import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { DevicesComponent } from './devices/devices.component';
import { AlarmsComponent } from './alarms/alarms.component';
import { TimersComponent } from './timers/timers.component';
import { ManageComponent } from './manage/manage.component';
import { FormsModule } from '@angular/forms';
import { MqttModule, IMqttServiceOptions } from 'ngx-mqtt';

const MQTT_SERVICE_OPTIONS: IMqttServiceOptions = {
  hostname: 'localhost',
  port: 9001, 
  protocol: 'ws',

};

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    DevicesComponent,
    AlarmsComponent,
    TimersComponent,
    ManageComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    MqttModule.forRoot(MQTT_SERVICE_OPTIONS),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
