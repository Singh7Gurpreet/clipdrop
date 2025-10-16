from bleak import BleakScanner, BleakClient

class BleClient:
    def __init__(self, service_uuid):
        self.service_uuid = service_uuid.lower()
        self.client = None
        self._callbacks = {}
        self._notify_chars = {}
        self._write_chars = {}

    async def connect(self, scan_timeout=10):
        print(f"🔍 Scanning for devices advertising {self.service_uuid}...")
        device = await BleakScanner.find_device_by_filter(
            lambda d, ad: self.service_uuid in [u.lower() for u in (ad.service_uuids or [])],
            timeout=scan_timeout
        )
        if device is None:
            raise RuntimeError("❌ No device found advertising the target service")

        print(f"✅ Found device: {device.name} [{device.address}]")
        self.client = BleakClient(device)
        await self.client.__aenter__()
        print("✅ Connected:", self.client.is_connected)

        service = self.client.services.get_service(self.service_uuid)
        if service is None:
            raise RuntimeError("❌ Service not found after connection")

        for char in service.characteristics:
            if "notify" in char.properties:
                self._notify_chars[char.uuid.lower()] = char
            if "write" in char.properties:
                self._write_chars[char.uuid.lower()] = char

        print("✅ Characteristics discovered:")
        for uuid in self._notify_chars: print(f"  - Notify: {uuid}")
        for uuid in self._write_chars: print(f"  - Write:  {uuid}")

    # register callback for received data on specific UUID
    def on_receive(self, uuid, callback):
        uuid = uuid.lower()
        self._callbacks[uuid] = callback

    async def start_notifications(self):
        for uuid, char in self._notify_chars.items():
            await self.client.start_notify(char, self._make_notifier(uuid))
            print(f"🔔 Listening to notifications on {uuid}")

    def _make_notifier(self, uuid):
        def _callback(sender, data):
            cb = self._callbacks.get(uuid)
            if cb:
                try:
                    cb(data.decode(errors="ignore"))
                except Exception as e:
                    print(f"⚠️ Error in callback for {uuid}: {e}")
            else:
                print(f"[Notify] {uuid}: {data}")
        return _callback

    async def emit(self, uuid, payload: str):
        uuid = uuid.lower()
        char = self._write_chars.get(uuid)
        if not char:
            raise ValueError(f"No writable characteristic for UUID {uuid}")
        await self.client.write_gatt_char(char, payload.encode(), response=True)
        print(f"[Python → BLE] {uuid}: {payload}")

    async def disconnect(self):
        if self.client:
            await self.client.__aexit__(None, None, None)
            print("🔌 Disconnected")
