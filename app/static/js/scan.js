(async function(){
    const preview = document.getElementById('preview');
    const codeReader = new ZXingBrowser.BrowserMultiFormatReader();
    const devices = await ZXingBrowser.BrowserCodeReader.listVideoInputDevices();
    const deviceId = devices[0]?.deviceId;
    if(!deviceId){ alert('No camera found'); return; }
    await codeReader.decodeFromVideoDevice(deviceId, preview, (res, err) => {
    if(res){ window.location.href = res.getText(); }
    });
})();