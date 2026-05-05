import { useEffect, useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useParams, useSearchParams } from "react-router-dom";
import api from "../services/api";

export default function Player() {
  const { slug } = useParams();
  const [searchParams] = useSearchParams();
  const phaseFromUrl = Number(searchParams.get("phase") || "1");
  const qc = useQueryClient();
  const [selectedPhase, setSelectedPhase] = useState(
    Number.isNaN(phaseFromUrl) || phaseFromUrl < 1 || phaseFromUrl > 5 ? 1 : phaseFromUrl,
  );
  const [answers, setAnswers] = useState(Array.from({ length: 30 }, () => -1));

  const { data: course } = useQuery({
    queryKey: ["course", slug],
    queryFn: async () => (await api.get(`/courses/${slug}/`)).data,
  });

  const { data: phasesData, refetch } = useQuery({
    queryKey: ["phases", slug],
    queryFn: async () => (await api.get(`/courses/${slug}/phases/`)).data,
  });

  const quizSubmit = useMutation({
    mutationFn: async () =>
      (
        await api.post(`/courses/${slug}/phases/${selectedPhase}/quiz/`, {
          answers,
        })
      ).data,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["phases", slug] });
      qc.invalidateQueries({ queryKey: ["enrollments"] });
    },
  });
  const markReading = useMutation({
    mutationFn: async () =>
      (await api.post(`/courses/${slug}/phases/${selectedPhase}/reading-complete/`)).data,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["phases", slug] });
    },
  });

  const phase = useMemo(
    () => (phasesData || []).find((p) => p.phase_number === selectedPhase),
    [phasesData, selectedPhase],
  );
  const quizQuestions = phase?.quiz_questions || [];

  useEffect(() => {
    setAnswers(Array.from({ length: 30 }, () => -1));
  }, [selectedPhase, slug]);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 grid lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2 space-y-4">
        <h1 className="text-xl font-semibold">{course?.title}</h1>
        <div className="rounded-xl border bg-white p-5">
          <h2 className="text-lg font-semibold">
            {phase?.title || `Phase ${selectedPhase}`} learning
          </h2>
          <p className="text-sm text-slate-600 mt-2 whitespace-pre-wrap">
            {phase?.content || "Select a phase from the right panel."}
          </p>
          <div className="mt-4">
            <h3 className="font-medium text-sm">Reading resources</h3>
            <ul className="mt-2 space-y-1 text-sm">
              {(phase?.resources?.reading || []).map((r, idx) => (
                <li key={idx}>
                  <a className="text-brand-700 underline" href={r.url} target="_blank" rel="noreferrer">
                    {r.title}
                  </a>
                </li>
              ))}
            </ul>
          </div>
          <div className="mt-4">
            <h3 className="font-medium text-sm">Video lectures</h3>
            <ul className="mt-2 space-y-1 text-sm">
              {(phase?.resources?.videos || []).map((v, idx) => (
                <li key={idx}>
                  <a className="text-brand-700 underline" href={v.url} target="_blank" rel="noreferrer">
                    {v.title}
                  </a>
                </li>
              ))}
            </ul>
          </div>
          <div className="mt-4">
            <h3 className="font-medium text-sm">Numerical learning checkpoints</h3>
            <ul className="mt-2 list-disc ml-5 text-sm text-slate-700 space-y-1">
              {(phase?.resources?.data_points || []).map((d, idx) => (
                <li key={idx}>{d}</li>
              ))}
            </ul>
          </div>
          <div className="mt-4">
            <h3 className="font-medium text-sm">Practice tasks</h3>
            <ul className="mt-2 list-disc ml-5 text-sm text-slate-700 space-y-1">
              {(phase?.resources?.practice_tasks || []).map((d, idx) => (
                <li key={idx}>{d}</li>
              ))}
            </ul>
          </div>
          <button
            type="button"
            className="mt-4 rounded-lg border border-brand-600 text-brand-700 px-3 py-2 text-sm"
            onClick={() => markReading.mutate()}
            disabled={markReading.isPending || phase?.progress?.reading_completed}
          >
            {phase?.progress?.reading_completed ? "Reading completed" : "Mark reading complete"}
          </button>
        </div>
        <div className="rounded-xl border bg-white p-4">
          <h2 className="font-medium">Quick quiz (30 MCQs)</h2>
          <p className="text-sm text-slate-600 mt-1">
            Submit 30 answers for this phase to unlock the next one.
          </p>
          <div className="mt-3 space-y-3 max-h-[440px] overflow-auto pr-1">
            {quizQuestions.length === 0 && (
              <p className="text-sm text-slate-500">Quiz will appear after enrollment and phase initialization.</p>
            )}
            {quizQuestions.map((q, i) => (
              <div key={i} className="border rounded-lg p-3">
                <p className="text-sm font-medium">
                  Q{i + 1}. {q.question}
                </p>
                <div className="mt-2 grid sm:grid-cols-2 gap-2">
                  {(q.options || []).map((opt, idx) => (
                    <label
                      key={idx}
                      className={`border rounded px-2 py-1 text-sm cursor-pointer ${
                        answers[i] === idx ? "border-brand-600 bg-brand-50" : ""
                      }`}
                    >
                      <input
                        type="radio"
                        name={`q-${i}`}
                        className="mr-2"
                        checked={answers[i] === idx}
                        onChange={() => {
                          const next = [...answers];
                          next[i] = idx;
                          setAnswers(next);
                        }}
                      />
                      {opt}
                    </label>
                  ))}
                </div>
              </div>
            ))}
          </div>
          <button
            type="button"
            className="mt-4 rounded-lg bg-brand-600 text-white px-4 py-2 font-medium"
            onClick={() => quizSubmit.mutate()}
            disabled={
              quizSubmit.isPending ||
              quizQuestions.length !== 30 ||
              answers.includes(-1) ||
              !phase?.progress?.reading_completed
            }
          >
            Submit phase quiz
          </button>
          {!phase?.progress?.reading_completed && (
            <p className="text-xs text-amber-700 mt-2">
              First complete the reading material for this phase, then attempt the quiz.
            </p>
          )}
          {quizSubmit.data && (
            <div className="text-sm mt-3 space-y-1 rounded-lg border border-slate-200 bg-slate-50 p-3">
              <p>
                Result: <strong>{quizSubmit.data.correct}</strong> correct ·{" "}
                <strong>{quizSubmit.data.wrong}</strong> wrong (out of{" "}
                {quizSubmit.data.total_questions ?? 30})
              </p>
              <p>
                Score: <strong>{quizSubmit.data.score_percent}%</strong> · Pass mark:{" "}
                <strong>{quizSubmit.data.pass_mark_percent ?? quizSubmit.data.required}%</strong> (need at least{" "}
                <strong>{quizSubmit.data.min_correct_required ?? "—"}</strong> correct)
              </p>
              <p className="font-medium">
                {quizSubmit.data.passed ? "Passed — next phase is unlocked." : "Not passed — review readings and try again."}
              </p>
            </div>
          )}
        </div>
      </div>
      <aside className="rounded-xl border bg-white p-4 h-fit">
        <h2 className="font-medium mb-2">5-phase roadmap</h2>
        <ul className="space-y-2 text-sm">
          {(phasesData || []).map((p) => (
            <li key={p.id}>
              <button
                type="button"
                onClick={() => setSelectedPhase(p.phase_number)}
                className={`w-full text-left border rounded-md p-2 ${
                  selectedPhase === p.phase_number ? "border-brand-600 bg-brand-50" : ""
                }`}
              >
                <div className="font-medium">Phase {p.phase_number}</div>
                <div className="text-xs text-slate-600 mt-1">{p.description}</div>
                <div className="text-xs mt-1">
                  {p.progress?.completed ? "Completed ✅" : "Pending"}
                </div>
              </button>
            </li>
          ))}
        </ul>
        <button type="button" className="mt-4 text-xs underline" onClick={() => refetch()}>
          Refresh progress
        </button>
      </aside>
    </div>
  );
}
