interface FieldErrorProps {
  id: string;
  message?: string;
}

export default function FieldError({ id, message }: FieldErrorProps) {
  if (!message) return null;

  return (
    <span id={id} role="alert" className="text-red-600 text-xs mt-1 block">
      {message}
    </span>
  );
}
