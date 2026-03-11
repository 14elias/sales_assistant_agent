interface Props {
  status: string;
}

export default function StatusIndicator({ status }: Props) {
  return (
    <div style={{ marginBottom: "10px" }}>
      Status: <b>{status}</b>
    </div>
  );
}