import { Link } from "react-router-dom";
export default function DataTable({ columns = [], rows = [] }){
  function renderCell(col, row){
    if (col.linkTo){
      const href = col.linkTo.replace(":id", row.id);
      const label = col.linkLabel ? col.linkLabel(row) : "Ver";
      return <Link className="underline" to={href}>{label}</Link>;
    }
    let v = typeof col.render === "function" ? col.render(row) : row[col.key];
    if (typeof v === "boolean") v = v ? "✓" : "—";
    return v;
  }
  return (
    <div className="overflow-x-auto rounded-xl border border-white/10">
      <table className="min-w-full text-sm">
        <thead className="bg-white/5">
          <tr>{columns.map((c) => (<th key={c.key || c.label} className="text-left px-3 py-2 font-semibold">{c.label}</th>))}</tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={r.id || i} className="border-t border-white/5">
              {columns.map((c) => (
                <td key={c.key || c.label} className="px-3 py-2">{renderCell(c, r)}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
