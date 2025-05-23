import { useState } from "react";
import * as XLSX from "xlsx";

export default function Home() {
  const [fileName, setFileName] = useState("");

  const handleUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFileName(file.name);
    }
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>지구스토어 특가 대시보드</h1>
      <div style={{ margin: '1rem 0' }}>
        <label htmlFor="excel-upload" style={{ marginRight: '0.5rem' }}>
          📁 엑셀 파일 업로드:
        </label>
        <input id="excel-upload" type="file" onChange={handleUpload} />
      </div>
      {fileName && <p>선택된 파일: {fileName}</p>}
    </div>
  );
}
