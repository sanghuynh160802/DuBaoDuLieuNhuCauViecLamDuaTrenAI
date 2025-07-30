import axiosApiInstance from "../api"
import { ILogin,ISignUp, ISendMail, IUpdate } from "../types/user"
import { IJob } from "../types/auth"

export const refreshAccessToken = async (): Promise<any> => {
    const refresh_token = localStorage.getItem("refresh_token")
    const data = {
        refresh_token: refresh_token,
    }
    return await axiosApiInstance.post("/auth/refresh", data)
}
export const loginApi = async (data: ILogin) => {
    // return await axiosApiInstance.post("/auth/login", data)
    return await axiosApiInstance.post("http://localhost:3009/auth/login", data)
}
export const registerApi = async (data: ISignUp) => {
    return await axiosApiInstance.post("/auth/register", data)
}
export const sendMailApi = async (data: ISendMail) => {
    return await axiosApiInstance.post("/auth/sendMail", data )
}
export const forgotpassword = async (email: string) => {
    return await axiosApiInstance.post("/auth/forgotpassword", {email} )
}
export const resetpassword = async (email: string, password: string) => {
    return await axiosApiInstance.post("/auth/resetpassword", {email,password} )
}
export const deleteAPI = async (id: string) => {
    return await axiosApiInstance.delete(`/auth/${id}`)
}
export const createJob = async (jobData: IJob) => {
  return await axiosApiInstance.post('/app/jobs', jobData);
};
export const getJobAll = async () => {
    // return await axiosApiInstance.get('/app/dataCrawl');
    return await axiosApiInstance.get('http://localhost:3009/app/dataCrawl');
}
export const getJobID = async (id: string) => {
    // return await axiosApiInstance.get(`/app/dataCrawl/${id}`)
    return await axiosApiInstance.get(`http://localhost:3009/app/dataCrawl/${id}`)
}
export const getJobTitle = async () => {
    return await axiosApiInstance.get("/app/jobtitle")
}
export const getJobFilter = async (
  keyFilter1: string, 
  keyFilter2: string, 
  keyFilter3: string,
  level: string,
  workWay: string,
  education: string,
  experience: string,
  salary: number | null // thêm param
) => {
  return await axiosApiInstance.get(`/app/filterjob`, {
    params: {
      key1: keyFilter1,
      key2: keyFilter2,
      key3: keyFilter3,
      level,
      workWay,
      education,
      experience,
      salary,
    }
  });
};
export const getProfessions = async () => {
    try {
      const response = await axiosApiInstance.get("http://localhost:3009/app/professions");
      return response.data.data; // Only return the array of professions
    } catch (error) {
      console.error("Error fetching professions:", error);
      throw error;
    }
};
export const getAllLevels = async (): Promise<string[]> => {
    try {
      const response = await axiosApiInstance.get("http://localhost:3009/app/levels");
      return response.data.data.map((item: { Level: string }) => item.Level); // Return array of strings
    } catch (error) {
      console.error("Error fetching levels:", error);
      throw error;
    }
};  
export const getAllWorkWays = async (): Promise<string[]> => {
    try {
      const response = await axiosApiInstance.get("http://localhost:3009/app/workways");
      return response.data.data.map((item: { Work_Way: string }) => item.Work_Way);
    } catch (error) {
      console.error("Error fetching work ways:", error);
      throw error;
    }
};
export const getAllEducation = async (): Promise<string[]> => {
    try {
      const response = await axiosApiInstance.get("http://localhost:3009/app/education");
      return response.data.data.map((item: { Education: string }) => item.Education);
    } catch (error) {
      console.error("Error fetching education levels:", error);
      throw error;
    }
};
export const getAllExperiences = async (): Promise<string[]> => {
    try {
      const response = await axiosApiInstance.get("http://localhost:3009/app/experiences");
      console.log("✅ Loaded experience levels:", response.data.data);
      return response.data.data;
    } catch (error) {
      console.error("❌ Error fetching experiences:", error);
      throw error;
    }
  };  
  
// export const getInfo = async () => {
//     return await axiosApiInstance.get("/users/me")
// }
export const getInfo = async () => {
    try {
        const response = await axiosApiInstance.get("http://localhost:3009/users/me");
        return response;
    } catch (error) {
        console.error("Error fetching user info:", error);
        throw error;
    }
}
export const getInfoAll = async () => {
    //return await axiosApiInstance.get("/users/")
    return await axiosApiInstance.get("http://localhost:3009/users/")
}
export const updateInfo = async (data: IUpdate) => {
  return await axiosApiInstance.put(`/users/${data.id}`, data) // Use the user ID in the URL
}
export const updateJob = async (id: string, data: IJob) => {
    return await axiosApiInstance.put(`/app/updatejob/${id}`, data)
}
// New method to fetch top 20 jobs data from Flask API
export const getTopJobs = async () => {
    return await axiosApiInstance.get("http://localhost:5000/api/top-jobs");
}
// New method to fetch all cities from Flask API
export const getCities = async () => {
    return await axiosApiInstance.get("http://localhost:5000/api/cities");
}
// Fetch job prediction results from Flask API
export const getJobPredictions = async (city: string, job: string, time: string, step: number = 12) => {
    try {
        const response = await axiosApiInstance.post("http://localhost:5000/api/predict", {
            city,
            job,
            time,
            step
        });
        return response.data;
    } catch (error) {
        console.error("Error fetching job predictions:", error);
        throw error;
    }
};
export const getUserIdByName = async (name: string): Promise<number | null> => {
    try {
      const encodedName = encodeURIComponent(name);
      const response = await axiosApiInstance.get(`http://localhost:3009/users/get-id-by-name/${encodedName}`);
      return response.data.id; // ID if found
    } catch (error: any) {
      console.error("Error fetching user ID by name:", error);
      return null; // Or throw error if you want to handle it differently
    }
};
export const getCVsByApplicantID = async (applicantId: string) => {
  return await axiosApiInstance.get(`/app/cv/applicant/id/${applicantId}`);
}
// 🆕 NEW: Get all CVs by company ID
export const getCVsByCompanyId = async (companyId: string) => {
    return await axiosApiInstance.get(`/app/cv/company/id/${companyId}`);
}

// 🆕 NEW: Get all CVs by company Name (if you need it later)
export const getCVsByCompanyName = async (companyName: string) => {
    return await axiosApiInstance.get(`/app/cv/company/name/${companyName}`);
}

export const updateCVStatusApi = async (id: string, status: 'REVIEWED' | 'ACCEPTED' | 'REJECTED') => {
    const body = { status };
    return await axiosApiInstance.put(`/app/cv/status/${id}`, body);
}

export const getSourcePictureByCompanyName = async (companyName: string) => {
  return await axiosApiInstance.get(`/app/source-picture`, {
    params: { companyName }
  });
};

export const saveEmployerMessageApi = async (submissionId: string, message: string) => {
  return await axiosApiInstance.put(`/app/cv-submission/${submissionId}/message`, {
    message
  });
};

// New service functions for crawling using fetch
const CRAWLING_API_BASE_URL = "http://localhost:5000/api";

export const crawlJobUrlsItviec = async (signal: AbortSignal) => {
    const response = await fetch(`${CRAWLING_API_BASE_URL}/run-script/crawl-job-urls-itviec`, {
        method: "POST",
        signal: signal,
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response;
};

export const crawlJobInfoItviec = async (signal: AbortSignal) => {
    const response =  await fetch(`${CRAWLING_API_BASE_URL}/run-script/crawl-job-info-itviec`, {
        method: "POST",
        signal: signal,
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response;
};

export const crawlJobUrlsTopdev = async (signal: AbortSignal) => {
  const response = await fetch(`${CRAWLING_API_BASE_URL}/run-script/crawl-job-urls-topdev`, {
      method: "POST",
      signal: signal,
  });
  if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response;
};

export const crawlJobInfoTopdev = async (signal: AbortSignal) => {
  const response =  await fetch(`${CRAWLING_API_BASE_URL}/run-script/crawl-job-info-topdev`, {
      method: "POST",
      signal: signal,
  });
  if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response;
};

export const crawlJobUrlsVieclam24h = async (signal: AbortSignal) => {
  const response = await fetch(`${CRAWLING_API_BASE_URL}/run-script/crawl-job-urls-vieclam24h`, {
      method: "POST",
      signal: signal,
  });
  if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response;
};

export const crawlJobInfoVieclam24h = async (signal: AbortSignal) => {
  const response =  await fetch(`${CRAWLING_API_BASE_URL}/run-script/crawl-job-info-vieclam24h`, {
      method: "POST",
      signal: signal,
  });
  if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response;
};

// user.service.ts
export const stopCrawling = async (scriptKey: string) => {
  try {
      const response = await fetch(`${CRAWLING_API_BASE_URL}/stop-script/${scriptKey}`, {
          method: "POST",
      });
      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
  } catch (error) {
      console.error("Error stopping crawling:", error);
      throw error;
  }
};

export const createUserSkill = async (data: {
  user_id: string;
  level: string;
  skill: string;
  experience: string;
  work_way: string;
  city: string;
}) => {
  return await axiosApiInstance.post("http://localhost:3009/app/user-skill", data);
};

// Get user skills by user ID
export const getUserSkillsByUserId = async (user_id: string) => {
  return await axiosApiInstance.get(`http://localhost:3009/app/user-skill/${user_id}`);
};

// Get matched jobs by user ID
export const getJobsByUserId = async (user_id: string) => {
  try {
    const response = await axiosApiInstance.get(`http://localhost:3009/app/jobs-by-user/${user_id}`);
    return response.data;
  } catch (error) {
    console.error("Failed to fetch matched jobs:", error);
    throw error;
  }
};

// Get matched jobs by job ID
export const getJobsByJobId = async (job_id: string) => {
  try {
    const response = await axiosApiInstance.get(`http://localhost:3009/app/jobs-by-job/${job_id}`);
    return response.data;
  } catch (error) {
    console.error("Failed to fetch matched jobs:", error);
    throw error;
  }
};

export const fetchJobsForUser = async (user_id: string) => {
  try {
    const response = await axiosApiInstance.get(`/app/jobs/user/${user_id}`);
    return response.data;
  } catch (error) {
    console.error("Failed to fetch jobs for user:", error);
    throw error;
  }
};

// Save a job post
export const savePost = async (data: {
  user_id: string;
  post_id: string;
}) => {
  return await axiosApiInstance.post("http://localhost:3009/app/save-post", data);
};

// Get saved posts by user ID
export const getSavedPostsByUserId = async (user_id: string) => {
  return await axiosApiInstance.get(`http://localhost:3009/app/save-post/${user_id}`);
};

// Delete a saved post by post_id only
export const deleteSavedPostByPostId = async (post_id: string) => {
  return await axiosApiInstance.delete(`http://localhost:3009/app/save-post/${post_id}`);
};

export const getUserById = async (id: string) => {
  return await axiosApiInstance.get(`/users/${id}`);
}

export const getIndustryFields = async (): Promise<string[]> => {
  try {
    const response = await axiosApiInstance.get("http://localhost:3009/app/industry-fields");
    return response.data;
  } catch (error) {
    console.error("Failed to fetch industry fields:", error);
    throw error;
  }
};