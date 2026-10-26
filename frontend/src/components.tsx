import type { ReactNode } from "react";

export const label = (v: string) => v.replace(/_/g, " ");

export function Badge({ value }: { value: string }) {
  return <span className={`badge badge-${value}`}>{label(value)}</span>;
}

export function Modal({ title, onClose, children }: { title: string; onClose: () => void; children: ReactNode }) {
  return (
    <div className="overlay" onMouseDown={onClose}>
      <div className="modal" role="dialog" aria-modal="true" aria-label={title} onMouseDown={(e) => e.stopPropagation()}>
        <h2>{title}</h2>
        {children}
      </div>
    </div>
  );
}

export function Field({ name, children }: { name: string; children: ReactNode }) {
  return (
    <label className="field">
      <span>{name}</span>
      {children}
    </label>
  );
}

export function Select<T extends string>({
  value,
  options,
  onChange,
  required,
}: {
  value: T;
  options: readonly T[];
  onChange: (v: T) => void;
  required?: boolean;
}) {
  return (
    <select value={value} required={required} onChange={(e) => onChange(e.target.value as T)}>
      {options.map((o) => (
        <option key={o} value={o}>
          {label(o)}
        </option>
      ))}
    </select>
  );
}

export function FilterSelect({
  placeholder,
  value,
  options,
  onChange,
}: {
  placeholder: string;
  value: string;
  options: readonly string[];
  onChange: (v: string) => void;
}) {
  return (
    <select value={value} onChange={(e) => onChange(e.target.value)} aria-label={placeholder}>
      <option value="">{placeholder}</option>
      {options.map((o) => (
        <option key={o} value={o}>
          {label(o)}
        </option>
      ))}
    </select>
  );
}

export const toNum = (s: string): number | null => (s.trim() === "" ? null : Number(s));
export const fmtDate = (iso: string) => new Date(iso).toLocaleString();
