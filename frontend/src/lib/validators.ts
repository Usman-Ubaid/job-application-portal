export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$/;

  if (email.indexOf("@") === -1) return false;

  if (!emailRegex.test(email)) return false;
  return true;
};

const ALLOWED_ROLES = ["SEEKER", "EMPLOYER"] as const;
export type UserRole = (typeof ALLOWED_ROLES)[number];

export function isValidRole(role: string): role is UserRole {
  return ALLOWED_ROLES.includes(role as UserRole);
}
