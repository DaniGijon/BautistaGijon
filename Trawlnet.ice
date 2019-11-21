// Trawlent Initial phase: introducing actors

module miModulo {
  interface Downloader {
    string addDownloadTask(string url);
  };

  interface Orchestrator {
    string downloadTask(string url);
  };
};
