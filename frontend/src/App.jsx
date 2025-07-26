import React, { useState } from "react";

// Spinner used for loading states
const Spinner = () => (
  <svg
    className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
  >
    <circle
      className="opacity-25"
      cx="12"
      cy="12"
      r="10"
      stroke="currentColor"
      strokeWidth="4"
    />
    <path
      className="opacity-75"
      fill="currentColor"
      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
    />
  </svg>
);

export default function App() {
  const [text, setText] = useState("");
  const [intent, setIntent] = useState("summarization");
  const [apiResponse, setApiResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    setApiResponse(null);

    const payload = {
      model_context: {
        task: "text_analysis",
        intent,
        user_role: "customer",
        language: "en",
      },
      input: { text },
    };

    try {
      const res = await fetch("http://localhost:8000/mcp/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status}`);
      }

      const data = await res.json();
      setApiResponse(data);
    } catch (err) {
      console.error("Fetch error:", err);
      setError("Failed to get response. Please ensure the local server is running.");
    } finally {
      setLoading(false);
    }
  };

  const renderParsedResponse = () => {
    if (!apiResponse || typeof apiResponse !== "object") {
      return <p className="text-red-600">Invalid response format.</p>;
    }

    const { summary, classification } = apiResponse;

    if (!summary && !classification) {
      return (
        <pre className="text-sm whitespace-pre-wrap break-words text-gray-700">
          {JSON.stringify(apiResponse, null, 2)}
        </pre>
      );
    }

    return (
      <div className="space-y-6 text-left">
        {summary && (
          <div>
            <h3 className="font-semibold text-lg text-indigo-600">Summary</h3>
            <p className="mt-2 text-gray-700 leading-relaxed">{summary}</p>
          </div>
        )}
        {classification && (
          <div>
            <h3 className="font-semibold text-lg text-indigo-600">Classification</h3>
            <div className="mt-2 bg-gray-100 p-4 rounded-lg space-y-2">
              {Object.entries(classification).map(([key, value]) => (
                <div key={key} className="flex justify-between">
                  <span className="font-medium text-gray-700 capitalize">{key}:</span>
                  <span className="text-gray-900 font-mono bg-gray-200 px-2 py-1 rounded-md text-sm">
                    {String(value)}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

  const renderResponseContent = () => {
    if (loading) {
      return (
        <div className="flex flex-col items-center justify-center h-full text-gray-500">
          <Spinner />
          <p className="mt-3">Processing...</p>
        </div>
      );
    }

    if (error) {
      return (
        <div className="bg-red-100 border border-red-400 text-red-600 p-4 rounded-lg" role="alert">
          <p className="font-bold mb-2">Error</p>
          <p className="text-sm">{error}</p>
        </div>
      );
    }

    if (apiResponse) {
      return renderParsedResponse();
    }

    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        <p>Your results will appear here.</p>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
      <div className="container mx-auto p-4 sm:p-6 lg:p-8">
        <header className="text-center mb-10">
          <h1 className="text-4xl font-bold text-indigo-600">MCP Text Insight</h1>
          <p className="text-lg text-gray-600 mt-2">
            Analyze your text for summarization and classification.
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Card */}
          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
            <div className="space-y-6">
              <div>
                <label htmlFor="text-input" className="block text-sm font-medium text-gray-700 mb-1">
                  Your Text
                </label>
                <textarea
                  id="text-input"
                  className="w-full bg-white border border-gray-300 text-gray-900 rounded-md shadow-sm p-3 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  rows={8}
                  placeholder="Enter your text, feedback, or article here..."
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                />
              </div>

              <div>
                <label htmlFor="intent-select" className="block text-sm font-medium text-gray-700 mb-1">
                  Analysis Intent
                </label>
                <select
                  id="intent-select"
                  className="w-full bg-white border border-gray-300 text-gray-900 rounded-md shadow-sm p-3 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  value={intent}
                  onChange={(e) => setIntent(e.target.value)}
                >
                  <option value="summarization">Summarization</option>
                  <option value="classification">Classification</option>
                  <option value="summarization + classification">Summarization + Classification</option>
                </select>
              </div>

              <button
                className="w-full flex items-center justify-center bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-4 py-3 rounded-md transition-all duration-150 ease-in-out disabled:opacity-70 disabled:cursor-not-allowed"
                onClick={handleSubmit}
                disabled={loading || !text}
              >
                {loading ? <Spinner /> : "Analyze Text"}
              </button>
            </div>
          </div>

          {/* Output Card */}
          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
            <h2 className="text-xl font-semibold mb-4 text-gray-800 border-b border-gray-200 pb-3">
              Analysis Result
            </h2>
            <div className="mt-4 bg-gray-50 rounded-lg p-6 min-h-[300px] flex flex-col justify-center">
              {renderResponseContent()}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
