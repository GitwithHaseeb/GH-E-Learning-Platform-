import React from "react";

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error) {
    return { error };
  }

  componentDidCatch(error, info) {
    console.error(error, info);
  }

  render() {
    if (this.state.error) {
      return (
        <div className="max-w-xl mx-auto p-8">
          <h1 className="text-xl font-semibold text-red-700">Kuch galat ho gaya</h1>
          <p className="text-slate-600 mt-2">{String(this.state.error)}</p>
        </div>
      );
    }
    return this.props.children;
  }
}
