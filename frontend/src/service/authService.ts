import api from "../api/api";
import {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
} from "../types/auth";

export const login = async (
  data: LoginRequest
): Promise<LoginResponse> => {
  const formData = new URLSearchParams();

  formData.append("username", data.email);
  formData.append("password", data.password);

  const response = await api.post(
    "/users/login",
    formData,
    {
      headers: {
        "Content-Type":
          "application/x-www-form-urlencoded",
      },
    }
  );

  return response.data;
};

export const register = async (
  data: RegisterRequest
) => {
  const response = await api.post(
    "/users/register",
    data
  );

  return response.data;
};