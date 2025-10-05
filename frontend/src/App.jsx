import { useState } from "react";
import axios from "axios";
import Chat from './components/Chat';
import config from './config'; // Import the config

export default function App() {
  
  const [serviceName, setServiceName] = useState("");
  const [imageName, setImageName] = useState("");
  const [deployResult, setDeployResult] = useState("");

  const [logFile, setLogFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState("");

  const [recommendation, setRecommendation] = useState("");
  const [recommendInput, setRecommendInput] = useState("");

  // ---- API Calls ----
  const handleDeploy = async () => {
    try {
      const res = await axios.post(`${config.API_BASE}/deploy`, {
        service_name: serviceName,
        image: imageName,
      });
      setDeployResult(res.data.message || JSON.stringify(res.data));
    } catch (err) {
      setDeployResult("Error: " + err.message);
    }
  };

  const handleAnalyzeLogs = async () => {
    try {
      const formData = new FormData();
      formData.append("file", logFile);
      const res = await axios.post(`${config.API_BASE}/analyze-logs-upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      const result = res.data.analysis || JSON.stringify(res.data);
      setAnalysisResult(result);
      setRecommendInput(result); // Autofill recommend input with analysis result
    } catch (err) {
      setAnalysisResult("Error: " + err.message);
    }
  };

  const handleRecommend = async () => {
    try {
      const res = await axios.post(`${config.API_BASE}/recommend-actions`, {
        summary: recommendInput,
      });
      // Try to extract 'analysis' field from response
      let analysisText = "";
      try {
        const rec = res.data.recommendation || res.data;
        if (typeof rec === "string") {
          const parsed = JSON.parse(rec);
          analysisText = parsed.analysis || rec;
        } else if (rec.analysis) {
          analysisText = rec.analysis;
        } else {
          analysisText = JSON.stringify(rec);
        }
      } catch {
        analysisText = res.data.recommendation || JSON.stringify(res.data);
      }
      setRecommendation(analysisText);
    } catch (err) {
      setRecommendation("Error: " + err.message);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 p-8">
      <h1 className="text-4xl font-bold text-center mb-10 text-white flex items-center justify-center gap-3">
        <span>⚡</span> AIOps Copilot
        {config.ENV !== "production" && (
          <span className="text-sm bg-yellow-500 text-black px-2 py-1 rounded">
            {config.ENV}
          </span>
        )}
      </h1>
      <div className="max-w-4xl mx-auto">
        <Chat />
      </div>
    </div>
  );
}